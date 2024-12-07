from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    fee_for_returned_payment = fields.Boolean(
        string="Fee for Returned Payment",
        inverse="_inverse_fee_for_returned_payment",
        default=True
    )
    use_feature_fee_for_returned_payment = fields.Boolean(
        string="Is Fee for Returned Payment Available",
        related='company_id.use_feature_fee_for_returned_payment',
        readonly=True
    )

    def should_apply_return_fee(self):
        self.ensure_one()
        return self.use_feature_fee_for_returned_payment and self.fee_for_returned_payment

    @api.multi
    def _inverse_fee_for_returned_payment(self):
        for partner in self:
            if partner.child_ids:
                partner.child_ids.write({
                    "fee_for_returned_payment": partner.fee_for_returned_payment
                })
