from odoo import models, fields


class Settings(models.TransientModel):
    _inherit = "res.config.settings"

    use_feature_fee_for_returned_payment = fields.Boolean(
        string="Fee for the returned payment",
        related='company_id.use_feature_fee_for_returned_payment',
        help="Adds to Contracts (or an invoice) a fee given a confirmation of a returned payment.",
        readonly=False,
        required=True
    )
    journal_return_late_fee = fields.Many2one(
        'account.journal',
        related='company_id.journal_return_late_fee',
        string="Journal",
        help="Journal for the fee to be created at when creating a plain invoice.",
        readonly=False,
        required=True
    )
    product_return_late_fee = fields.Many2one(
        'product.product',
        related='company_id.product_return_late_fee',
        string="Fee for the returned payment",
        help="Select the product that will be added to Contracts triggered by the confirmation of a returned payment.",  # noqa: E501
        readonly=False,
        required=True
    )
