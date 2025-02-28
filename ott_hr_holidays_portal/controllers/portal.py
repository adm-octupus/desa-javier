# -*- coding: utf-8 -*-
# from odoo import http
from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime, time

class LeavePortal(CustomerPortal):


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        HrLeave = request.env['hr.leave']
        if 'leave_count' in counters:
            values['leave_count'] = HrLeave.search_count(self._prepare_hr_leave_domain(partner)) \
                if HrLeave.check_access_rights('read', raise_exception=False) else 0
        return values

    def _prepare_hr_leave_domain(self, partner):
        return [
            ('employee_ids.address_home_id', '=', partner.id)
        ]

    @http.route(['/my/leaves', '/my/leaves/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leaves(self, page=1, date_from=None, date_to=None, search=None, search_in=None, sortby=None, filterby=None, **kw):
        Leave = request.env['hr.leave'].sudo()
        partner = request.env.user.partner_id
        domain = self._prepare_hr_leave_domain(partner)

        leaves = Leave.search(domain)

        values = {
            'leaves': leaves,
            'page_name': 'leaves',
            'default_url': '/my/leaves',
        }

        return request.render("ott_hr_holidays_portal.portal_my_leaves", values)


    @http.route('/my/leaves/new', type='http', auth='user', website=True)
    def portal_create_leave(self, **kwargs):
        domain = ['|', ('requires_allocation', '=', 'no'), '&', ('has_valid_allocation', '=', True), '&', ('virtual_remaining_leaves', '>', 0), ('max_leaves', '>', '0')]
        Leave = request.env['hr.leave'].sudo()
        from_period_selection = Leave._fields['request_date_from_period'].selection
        hour_from_selection = Leave._fields['request_hour_from'].selection
        hour_to_selection = Leave._fields['request_hour_to'].selection
        leave_types = request.env['hr.leave.type'].sudo().search(domain)
        return request.render('ott_hr_holidays_portal.portal_my_leave_form', {            
            'from_period_selection': from_period_selection,
            'hour_from_selection': hour_from_selection,
            'hour_to_selection': hour_to_selection,
            'leave_types': leave_types,
        })

    @http.route('/my/leaves/submit', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def portal_submit_leave(self, **post):
        try:
            Leave = request.env['hr.leave'].sudo()
            partner_id = request.env.user.partner_id.id
            employee = request.env['hr.employee'].sudo().search([('address_home_id', '=', partner_id)], limit=1)

            # Obtener datos del formulario
            leave_type_id_input = post.get('leave_type_id')
            date_from_input = post.get('date_from')
            date_to_input = post.get('date_to')
            hour_from = post.get('time_from')
            hour_to = post.get('time_to')
            decription_input = post.get('private_name')
            request_period = post.get('request_date_from_period')
            request_unit = post.get('request_unit')   

            if request_unit == 'day':
                date_from = datetime.strptime(date_from_input, '%Y-%m-%d')
                date_to = datetime.strptime(date_to_input, '%Y-%m-%d')

                attendance_from, attendance_to = Leave._get_attendances(employee, date_from, date_to)
                date_from = Leave._get_start_or_end_from_attendance(attendance_from.hour_from, date_from, employee)
                date_to = Leave._get_start_or_end_from_attendance(attendance_to.hour_to, date_to, employee)

                request.env['hr.leave'].sudo().create({
                    'holiday_status_id': int(leave_type_id_input),
                    'date_from': date_from,       
                    'date_to': date_to,
                    'request_date_from': date_from.date(),    
                    'request_date_to': date_to.date(),    
                    'employee_id': employee.id,
                    'private_name': decription_input,
                })

            elif request_unit == 'half_day':
                date_from = datetime.strptime(date_from_input, '%Y-%m-%d')
                date_to = datetime.strptime(date_from_input, '%Y-%m-%d')

                attendance_from, attendance_to = Leave._get_attendances(employee, date_from, date_to)

                if request_period == 'am':
                    hour_from = attendance_from.hour_from
                    hour_to = attendance_from.hour_to
                else:
                    hour_from = attendance_to.hour_from
                    hour_to = attendance_to.hour_to

                date_from = Leave._get_start_or_end_from_attendance(hour_from, date_from, employee)
                date_to = Leave._get_start_or_end_from_attendance(hour_to, date_to, employee)

                request.env['hr.leave'].sudo().create({
                        'holiday_status_id': int(leave_type_id_input),
                        'request_unit_half': True,
                        'date_from': date_from,       
                        'date_to': date_to,    
                        'request_date_from': date_from.date(),    
                        'request_date_to': date_to.date(),          
                        'employee_id': employee.id,
                        'private_name': decription_input,
                    })

            elif request_unit == 'hour':   
                date_from = datetime.strptime(date_from_input, '%Y-%m-%d')
                date_to = datetime.strptime(date_from_input, '%Y-%m-%d')
                date_from = Leave._get_start_or_end_from_attendance(hour_from, date_from.date(), employee)
                date_to = Leave._get_start_or_end_from_attendance(hour_to, date_to.date(), employee)

                request.env['hr.leave'].sudo().create({
                    'holiday_status_id': int(leave_type_id_input),
                    'request_unit_hours': True,
                    'date_from': date_from,       
                    'date_to': date_to,    
                    'request_date_from': date_from.date(),    
                    'request_date_to': date_to.date(),    
                    'request_hour_from': hour_from,       
                    'request_hour_to': hour_to,    
                    'employee_id': employee.id,
                    'private_name': decription_input,
                })

        except Exception as e:
            # Manejar errores de creación
            return request.redirect('/my/leaves/new?error=%s' % (e))

        # Redirigir a la página de ausencias
        return request.redirect('/my/leaves')