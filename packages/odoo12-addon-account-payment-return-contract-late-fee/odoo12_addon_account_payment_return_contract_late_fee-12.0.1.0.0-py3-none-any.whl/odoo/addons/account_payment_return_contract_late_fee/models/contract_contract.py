from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'contract.contract'

    @api.multi
    def add_return_late_fee(self):
        """ Adds a punctual fee line to a contract """
        contract_line_model = self.env['contract.line']
        late_fee_product = self.env.user.company_id.product_return_late_fee

        for contract in self:
            if contract.partner_id.should_apply_return_fee() and late_fee_product:
                contract_line_model.create(
                    {
                        'contract_id': contract.id,
                        'product_id': late_fee_product.id,
                        'name': late_fee_product.get_product_multiline_description_sale(),
                        'price_unit': late_fee_product.list_price,
                        'quantity': 1,
                        'date_start': fields.Date.today(),
                        'is_auto_renew': False,
                        'recurring_invoicing_type': 'pre-paid',
                        'recurring_interval': 1,
                        'recurring_rule_type': 'monthly',
                        'date_end': fields.Date.today()
                    }
                )
