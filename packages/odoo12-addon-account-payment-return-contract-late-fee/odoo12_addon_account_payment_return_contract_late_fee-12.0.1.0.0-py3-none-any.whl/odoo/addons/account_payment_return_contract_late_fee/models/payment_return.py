from odoo import models, fields, api, _


class PaymentReturn(models.Model):
    _inherit = 'payment.return'

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        if super(PaymentReturn, self).action_confirm():
            if self.company_id.use_feature_fee_for_returned_payment:
                for return_line in self.line_ids:
                    if return_line.partner_id and return_line.partner_id.should_apply_return_fee():
                        partner_contracts = self.env['contract.contract'].search(
                            [
                                '&',
                                '&',
                                ('contract_type', '=', 'sale'),
                                '|',
                                ('partner_id', 'parent_of', return_line.partner_id.id),
                                ('partner_id', 'child_of', return_line.partner_id.id),
                                '|',
                                ('date_end', '>=', fields.Date.today()),
                                '&',
                                ('date_end', '=', False),
                                ('recurring_next_date', '!=', False)
                            ],
                            order="create_date asc",
                            limit=1
                        )
                        contract_message_to_post = _(
                            "A late fee has been applied from this Payment Return: "
                            "<a href=# data-oe-model=payment.return data-oe-id={0}>{1}</a>"
                        ).format(
                            self.id,
                            self.name
                        )
                        message_to_post = _(
                            "A late fee has been applied to the partner in "
                            "<a href=# data-oe-model={0} data-oe-id={1}>{2}</a>"
                        )
                        if partner_contracts:
                            partner_contracts.add_return_late_fee()
                            message_to_post = message_to_post.format(
                                'contract.contract',
                                partner_contracts.id,
                                partner_contracts.name
                            )
                            partner_contracts.message_post(
                                subject=_("Return Contract Late Fee"),
                                body=contract_message_to_post,
                                message_type="notification"
                            )
                        else:
                            journal_return_late_fee = self.env.user.company_id.journal_return_late_fee
                            late_fee_product = self.env.user.company_id.product_return_late_fee
                            if journal_return_late_fee:
                                invoice = self.env['account.invoice']
                                created_invoice = invoice.create(
                                    {
                                        'type': 'out_invoice',
                                        'reference_type': 'none',
                                        'journal_id': journal_return_late_fee.id,
                                        'currency_id': self.env.user.company_id.currency_id.id,
                                        'partner_id': return_line.partner_id.id
                                    }
                                )
                                created_invoice._onchange_partner_id()
                                line = self.env['account.invoice.line'].create({
                                    'product_id': late_fee_product.id,
                                    'invoice_id': created_invoice.id,
                                    'name': late_fee_product.display_name,
                                    'price_unit': late_fee_product.lst_price,
                                    'account_id': journal_return_late_fee.default_credit_account_id.id
                                })
                                line._onchange_product_id()
                                line_name = late_fee_product.display_name
                                line_date = (return_line.date or self.date or fields.Date.today()).strftime(
                                    self.env["res.lang"]._lang_get(self.env.user.lang).date_format
                                )
                                line_concept = return_line.concept or ""
                                line.write({
                                    'name': f'{line_name} {line_date} {line_concept}'
                                })
                                created_invoice.compute_taxes()
                                created_invoice.action_invoice_open()
                                created_invoice.message_post(
                                    subject=_("Return Contract Late Fee"),
                                    body=contract_message_to_post,
                                    message_type="notification"
                                )
                                message_to_post = message_to_post.format(
                                    'account.invoice',
                                    created_invoice.id,
                                    created_invoice.number
                                )
                        self.message_post(
                            subject=_("Return Contract Late Fee"),
                            body=message_to_post,
                            message_type="notification"
                        )
