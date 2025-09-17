from odoo import api, fields, models, _

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    lch_process = fields.Char('Process', store=True, required=True)
    lch_area = fields.Char('Area', store=True, required=True)
    lch_section = fields.Char('Section', store=True, required=True)
    
    def name_get(self):
        """
        Extiende el nombre mostrado del departamento concatenando 3 campos
        adicionales sin romper el nombre jerárquico (padre / hijo).
        """
        extra_fields = ('lch_process', 'lch_area', 'lch_section')
        hierarchical = self.env.context.get('hierarchical_naming', True)

        if hierarchical:
            base_pairs = dict(super().name_get())
        else:
            base_pairs = {rec.id: (rec.name or "") for rec in self}

        result = []
        for rec in self:
            base = base_pairs.get(rec.id, rec.name or "")
            extras = []
            for fname in extra_fields:
                if fname in self._fields:  # aquí corregido
                    val = rec[fname]
                    if val:
                        extras.append(str(val))
            if extras:
                base = f"{base} / {' / '.join(extras)}"
            result.append((rec.id, base))

        return result

