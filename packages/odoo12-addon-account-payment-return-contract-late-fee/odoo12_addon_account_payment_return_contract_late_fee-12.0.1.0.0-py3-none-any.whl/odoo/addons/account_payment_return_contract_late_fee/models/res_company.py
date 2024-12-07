from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    use_feature_fee_for_returned_payment = fields.Boolean(
        string="Fee for the returned payment",
        help="Adds to Contracts (or an invoice) a fee given a confirmation of a returned payment."
    )
    journal_return_late_fee = fields.Many2one(
        'account.journal',
        string="Journal",
        help="Journal for the fee to be created at when creating a plain invoice."
    )
    product_return_late_fee = fields.Many2one(
        'product.product',
        string="Fee for the returned payment",
        help="Select the product that will be added to Contracts triggered by the confirmation of a returned payment."  # noqa: E501
    )
