# -*- coding: utf-8 -*-
# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Payment return late fee for contracts",
    "version": "12.0.1.0.0",
    "depends": ["account_payment_return", "contract"],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL
    """,
    "category": "Accounting & Finance",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-accounting",
    "license": "AGPL-3",
    "summary": """
        Payment return late fee for contracts.
    """,
    "data": [
        "views/res_partner_view.xml",
        "views/res_config_settings.xml",
    ],
    "application": False,
    "installable": True,
}
