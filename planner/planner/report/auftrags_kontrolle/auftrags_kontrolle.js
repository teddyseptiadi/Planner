// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Auftrags Kontrolle"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("Buchung von"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1,
            "width": "60px"
        },
        {
            "fieldname": "failed",
            "label": __("Zeige nur fehlgeschlagene"),
            "fieldtype": "Check",
        }
    ]
};
