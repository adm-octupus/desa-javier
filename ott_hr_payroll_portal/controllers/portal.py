# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from babel.dates import format_date
from dateutil.relativedelta import relativedelta

# import locale

class PayslipPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payslip_count' in counters:
            payslip_count = request.env['hr.payslip'].sudo().search_count([
                ('employee_id.address_home_id', '=', request.env.user.partner_id.id)
            ])
            values['payslip_count'] = payslip_count
        return values

    def _get_payslip_searchbar_sortings(self):
        return {
            'date_desc': {'label': _('Latest'), 'order':'date_from desc'},
            'date_asc': {'label': _('Oldest'), 'order':'date_from asc'}
        }

    def _get_payslip_searchbar_filters(self):
        return {
            'all': {'label': _('All')},
            'last_month': {'label': _('Last month')},
            'last_year': {'label': _('Last year')}
        }

    def _get_payslip_searchbar_inputs(self):
        return {
            'number': {'input': 'number', 'label': _('Reference')},
            'batch': {'input': 'batch', 'label': _('Batch')},
        }

    @http.route(['/my/payslips', '/my/payslips/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_payslips(self, page=1, date_from=None, date_to=None, search=None, search_in=None, sortby=None, filterby=None, **kw):
        Payslip = request.env['hr.payslip'].sudo()
        partner_id = request.env.user.partner_id.id

        if not sortby:
            sortby = 'date_desc'

        if not filterby:
            filterby = 'last_year'

        # Dominio basado en los filtros
        domain = [('employee_id.address_home_id', '=', partner_id)]

        # Lógica para aplicar los filtros
        if filterby == 'last_month':
            date_from = fields.Date.today() - relativedelta(months=1)
            domain.append(('date_from', '>=', date_from))
        elif filterby == 'last_year':
            start_of_current_year = fields.Date.today().replace(month=1, day=1)
            domain.append(('date_from', '>=', start_of_current_year))

        # Aplicar el filtro de búsqueda general
        if search:
            if search_in == 'number':
                domain.append(('number', 'ilike', search))
            elif search_in == 'batch':
                domain.append(('struct_id.name', 'ilike', search))

        searchbar_sortings = self._get_payslip_searchbar_sortings()
        sort_order = searchbar_sortings[sortby]['order']

        # Paginación
        total_payslips = Payslip.search_count(domain)
        pager = portal_pager(
            url="/my/payslips",
            total=total_payslips,
            page=page,
            step=10  # Número de registros por página
        )
        payslips = Payslip.search(domain, limit=10, offset=pager['offset'], order=sort_order)

        searchbar_filters = self._get_payslip_searchbar_filters()
        searchbar_inputs = self._get_payslip_searchbar_inputs()

        values = {
            'payslips': payslips,
            'page_name': 'payslip',
            'pager': pager,
            'date_from': date_from or '',
            'date_to': date_to or '',
            'search': search or '',
            'search_in': search_in or 'number',
            'sortby': sortby,
            'filterby': filterby,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'format_date': format_date,
            'default_url': '/my/payslips',
        }

        return request.render("ott_hr_payroll_portal.portal_my_payslips", values)

    @http.route(['/my/payslips/download/<int:payslip_id>'], type='http', auth="user", website=True)
    def portal_download_payslip(self, payslip_id, **kw):
        generic_name = "Payslip"

        payslip = request.env['hr.payslip'].sudo().browse(payslip_id)
        if not payslip or payslip.employee_id.address_home_id != request.env.user.partner_id:
            return request.redirect('/my/payslips')

        report = payslip.struct_id.report_id
        pdf_content, dummy = request.env['ir.actions.report'].sudo().with_context(lang=payslip.employee_id.address_home_id.lang)._render_qweb_pdf(report, payslip.id)
        pdf_name = safe_eval(report.print_report_name, {'object': payslip}) if report.print_report_name else generic_name

        return request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', f'attachment; filename="{pdf_name}.pdf"'),
        ])