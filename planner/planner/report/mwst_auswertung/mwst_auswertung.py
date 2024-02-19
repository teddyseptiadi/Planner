# Copyright (c) 2023-2024, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data
from frappe.utils import rounded

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    return [
        {"label": _("Sales Invoice"), "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 85},
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 90},
        {"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 90},
        {"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 150},
        {"label": _("Net Amount"), "fieldname": "net_amount", "fieldtype": "Currency", "width": 150},
        {"label": _("Tax Rate"), "fieldname": "tax_rate", "fieldtype": "Percent", "width": 150},
        {"label": _("tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 150}
    ]

def get_data(filters):
    
    invoices = frappe.db.sql("""
        SELECT `name`
        FROM `tabSales Invoice`
        WHERE `posting_date` BETWEEN "2024-01-01" AND "2024-01-31"
          AND `docstatus` = 1;
        """, as_dict=True)
        
    data = []

    for i in invoices:
        doc = frappe.get_doc("Sales Invoice", i['name'])
        item_taxes, net_amounts = get_itemised_tax_breakup_data(doc)
        for k,v in item_taxes.items():
            for j in doc.items:
                if j.item_code == k:
                    account = j.income_account
                    amount = j.net_amount
            tax_amount = 0
            tax_rate = 0
            for tk, tv in v.items():
                if tv.get("tax_amount"):
                    tax_amount = tv.get("tax_amount")
                    tax_rate = tv.get("tax_rate")
            data.append({
                'sales_invoice':  doc.name,
                'date': doc.posting_date,
                'item_code': k,
                'account': account,
                'net_amount': amount,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount
            })
            
    return data
