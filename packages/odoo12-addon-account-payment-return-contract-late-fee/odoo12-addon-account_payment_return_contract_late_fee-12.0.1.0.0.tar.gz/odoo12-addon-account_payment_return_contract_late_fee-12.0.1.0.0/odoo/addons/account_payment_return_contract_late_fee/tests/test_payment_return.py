from odoo.tests.common import SavepointCase, tagged
from odoo.tests import tagged


@tagged("post_install", "account_payment_return_contract_late_fee")
class TestPaymentReturn(SavepointCase):
    @classmethod
    def setUpClass(self):
        super(TestPaymentReturn, self).setUpClass()

        self.account_type = self.env['account.account.type'].create({
            'name': 'Test',
            'type': 'receivable',
        })
        self.account = self.env['account.account'].create({
            'name': 'Test account',
            'code': 'TEST',
            'user_type_id': self.account_type.id,
            'reconcile': True,
            'currency_id': self.env.user.company_id.currency_id.id,
        })
        self.journal = self.env['account.journal'].create({
            'name': 'Test Sales Journal',
            'code': 'tVEN',
            'type': 'sale',
            'update_posted': True,
            'currency_id': self.env.user.company_id.currency_id.id,
            'default_credit_account_id': self.account.id,
        })
        self.partner_expense = self.env['res.partner'].create({'name': 'PE'})
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Test Bank Journal',
            'code': 'BANK',
            'type': 'bank',
            'update_posted': True,
            'default_expense_account_id': self.account.id,
            'default_expense_partner_id': self.partner_expense.id,
        })
        self.account_income = self.env['account.account'].create({
            'name': 'Test income account',
            'code': 'INCOME',
            'user_type_id': self.env['account.account.type'].create(
                {'name': 'Test income'}).id,
        })

        self.pricelist = self.env['product.pricelist'].create({
            'name': 'pricelist for contract test',
        })
        self.partner = self.env['res.partner'].create({
            'name': 'partner test contract',
            'property_product_pricelist': self.pricelist.id,
            'email': 'demo@demo.com'
        })

        self.main_product = self.env.ref('product.product_product_1')
        self.late_fee_product = self.env.ref('product.product_product_2')

        self.env.user.company_id.invoice_reference_type = 'invoice_number'
        self.env.user.company_id.product_return_late_fee = self.late_fee_product.id
        self.env.user.company_id.journal_return_late_fee = self.journal.id
        self.env.user.company_id.use_feature_fee_for_returned_payment = True

        self.contract = self.env['contract.contract'].create(
            {
                'name': 'Test Contract',
                'partner_id': self.partner.id,
                'contract_type': 'sale',
                'journal_id': self.journal.id,
                'contract_line_ids': [
                    (
                        0,
                        0,
                        {
                            'product_id': self.main_product.id,
                            'name': 'Services from #START# to #END#',
                            'quantity': 1,
                            'uom_id': self.main_product.uom_id.id,
                            'price_unit': 100,
                            'discount': 50,
                            'recurring_rule_type': 'monthly',
                            'recurring_interval': 1,
                            'date_start': '2024-10-15',
                            'recurring_next_date': '2024-10-16',
                        },
                    )
                ],
            }
        )

        self.contract.recurring_create_invoice()
        self.invoice = self.contract._get_related_invoices()[0]

        self.reason = self.env['payment.return.reason'].create({
            'code': 'RTEST',
            'name': 'Reason Test'
        })
        self.invoice.action_invoice_open()
        self.receivable_line = self.invoice.move_id.line_ids.filtered(
            lambda x: x.account_id.internal_type == 'receivable')
        # Invert the move to simulate the payment
        self.payment_move = self.invoice.move_id.copy({
            'journal_id': self.bank_journal.id
        })
        for move_line in self.payment_move.line_ids:
            move_line.with_context(check_move_validity=False).write({
                'debit': move_line.credit, 'credit': move_line.debit})
        self.payment_line = self.payment_move.line_ids.filtered(
            lambda x: x.account_id.internal_type == 'receivable')
        # Reconcile both
        (self.receivable_line | self.payment_line).reconcile()
        # Create payment return
        self.payment_return = self.env['payment.return'].create(
            {
                'journal_id': self.bank_journal.id,
                'line_ids': [
                    (
                        0,
                        0,
                        {
                            'date': '2024-10-15',
                            'partner_id': self.partner.id,
                            'move_line_ids': [(6, 0, self.payment_line.ids)],
                            'amount': self.payment_line.credit,
                            'expense_account': self.account.id,
                            'expense_amount': 10.0,
                            'expense_partner_id': self.partner.id
                        }
                    )
                ]
            }
        )

    def _get_mail_messages_prev(self, record):
        return self.env["mail.message"].search([
            ("model", "=", record._name),
            ("res_id", "=", record.id),
        ]).ids

    def _get_mail_messages(self, exclude_ids, record):
        return self.env["mail.message"].search([
            ("model", "=", record._name),
            ("res_id", "=", record.id),
            ('id', 'not in', exclude_ids)
        ])

    def test_confirm_return(self):
        self.payment_return.action_confirm()

    def test_confirm_fee_added(self):
        self.payment_return.action_confirm()
        self.assertIn(self.late_fee_product.id, self.contract.contract_line_ids.mapped('product_id').ids)

    def test_confirm_posted_messages_contract(self):
        exclude_ids = self._get_mail_messages_prev(self.contract)
        self.payment_return.action_confirm()
        mail_messages = self._get_mail_messages(exclude_ids, self.contract)
        self.assertGreaterEqual(
            len(mail_messages),
            1,
            "A chatter message must appear in contract.contract when payment.return confirmation is triggered"
        )

    def test_confirm_posted_messages_invoice(self):
        for contract in self.env['contract.contract'].search([('partner_id', '=', self.partner.id)]):
            contract.unlink()

        invoices_before = self.env['account.invoice'].search([('partner_id', '=', self.partner.id)])

        self.payment_return.action_confirm()

        new_invoice = self.env['account.invoice'].search(
            [
                ('partner_id', '=', self.partner.id),
                ('id', 'not in', invoices_before.ids if invoices_before else [])
            ],
            limit=1
        )
        mail_messages = self._get_mail_messages([], new_invoice)
        self.assertGreaterEqual(
            len(mail_messages),
            3,
            "A chatter message must appear in account.invoice when payment.return confirmation is triggered"
        )

    def test_confirm_posted_messages_payment_return(self):
        exclude_ids = self._get_mail_messages_prev(self.payment_return)
        self.payment_return.action_confirm()
        mail_messages = self._get_mail_messages(exclude_ids, self.payment_return)
        self.assertGreaterEqual(
            len(mail_messages),
            2,
            "A chatter message must appear in the payment.return when confirmation is triggered"
        )

    def test_confirm_invoice_created(self):
        for contract in self.env['contract.contract'].search([('partner_id', '=', self.partner.id)]):
            contract.unlink()

        invoices_before = self.env['account.invoice'].search([('partner_id', '=', self.partner.id)])

        self.payment_return.action_confirm()

        new_invoices = self.env['account.invoice'].search(
            [
                ('partner_id', '=', self.partner.id),
                ('id', 'not in', invoices_before.ids if invoices_before else [])
            ]
        )
        self.assertTrue(new_invoices, "No invoice were created when the payment return became confirmed.")
        self.assertTrue(
            not len(new_invoices) > 1,
            "More than one invoice were generated after return payment confirmation."
        )
        invoice = new_invoices
        late_fee_line = self.env['account.invoice.line'].search(
            [
                ('invoice_id', '=', invoice.id),
                ('product_id', '=', self.late_fee_product.id)
            ],
            limit=1
        )
        self.assertTrue(
            late_fee_line,
            "Late fee invoicing line is not present in the invoice generated."
        )
        self.assertTrue(
            late_fee_line.product_id.id == self.late_fee_product.id,
            "Late fee product in created invoice line is not present."
        )
