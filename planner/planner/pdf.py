# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, libracore and contributors
# For license information, please see license.txt
#

# imports
import frappe
from datetime import datetime
from frappe.utils.file_manager import save_file

# async background pdf creationg
@frappe.whitelist()
def enqueue_create_pdf(doctype, docname):
    frappe.enqueue(method=create_pdf, queue='long', timeout=300,
        **{'doctype': doctype, 'docname': docname})
    return

#background printing to attachment
def create_pdf(doctype, docname):
    from erpnextswiss.erpnextswiss.finance import get_account_sheets
    account_sheets = get_account_sheets(docname)
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="generator" content="frappe">
            <link type="text/css" rel="stylesheet" href="/assets/css/printview.css"><style>
            @media screen {
            .print-format-gutter {
                background-color: #d1d8dd;
                padding: 30px 0px;
            }
            .print-format {
                background-color: white;
                box-shadow: 0px 0px 9px rgba(0,0,0,0.5);
                max-width: 8.3in;
                min-height: 11.69in;
                padding: 0.75in;
                margin: auto;
            }

            .print-format.landscape {
                max-width: 11.69in;
                padding: 0.2in;
            }

            .page-break {
                padding: 30px 0px;
                border-bottom: 1px dashed #888;
            }

            .page-break:first-child {
                padding-top: 0px;
            }

            .page-break:last-child {
                border-bottom: 0px;
            }

            /* mozilla hack for images in table */
            body:last-child .print-format td img {
                width: 100% !important;
            }

            @media(max-width: 767px) {
                .print-format {
                    padding: 0.2in;
                }
            }
        }

        @media print {
            .print-format p {
                margin-left: 1px;
                margin-right: 1px;
            }
        }

        .data-field {
            margin-top: 5px;
            margin-bottom: 5px;
        }

        .data-field .value {
            word-wrap: break-word;
        }

        .important .value {
            font-size: 120%;
            font-weight: bold;
        }

        .important label {
            line-height: 1.8;
            margin: 0px;
        }

        .table {
            margin: 20px 0px;
        }

        .square-image {
            width: 100%;
            height: 0;
            padding: 50% 0;
            background-size: contain;
            /*background-size: cover;*/
            background-repeat: no-repeat !important;
            background-position: center center;
            border-radius: 4px;
        }

        .print-item-image {
            object-fit: contain;
        }

        .pdf-variables,
        .pdf-variable,
        .visible-pdf {
            display: none !important;
        }

        .print-format {
            font-size: 9pt;
            font-family: Helvetica, sans-serif;
            -webkit-print-color-adjust:exact;
        }

        .page-break {
            page-break-after: always;
        }

        .print-heading {
            border-bottom: 1px solid #aaa;
            margin-bottom: 10px;
        }

        .print-heading h2 {
            margin: 0px;
        }
        .print-heading h4 {
            margin-top: 5px;
        }

        table.no-border, table.no-border td {
            border: 0px;
        }

        .print-format label {
            /* wkhtmltopdf breaks label into multiple lines when it is inline-block */
            display: block;
        }

        .print-format img {
            max-width: 100%;
        }

        .print-format table td > .primary:first-child {
            font-weight: bold;
        }

        .print-format td, .print-format th {
            vertical-align: top !important;
            padding: 6px !important;
        }

        .print-format p {
            margin: 3px 0px 3px;
        }

        table td div {
            
            /* needed to avoid partial cutting of text between page break in wkhtmltopdf */
            page-break-inside: avoid !important;
            
        }

        /* hack for webkit specific browser */
        @media (-webkit-min-device-pixel-ratio:0) {
            thead, tfoot {
                display: table-header-group;
            }
        }

        [document-status] {
            margin-bottom: 5mm;
        }

        .signature-img {
            background: #fff;
            border-radius: 3px;
            margin-top: 5px;
            max-height: 150px;
        }

        .print-format [data-fieldtype="Table"] {
            overflow: auto;
        }
        .print-heading {
            text-align: right;
            text-transform: uppercase;
            color: #666;
            padding-bottom: 20px;
            margin-bottom: 20px;
            border-bottom: 1px solid #d1d8dd;
        }

        .print-heading h2 {
            font-size: 24px;
        }

        .print-format th {
            background-color: #eee !important;
            border-bottom: 0px !important;
        }

        /* modern format: for-test */
            </style>
        </head>
        <body>
            <div class="print-format-gutter">
                <div class="print-format">
    """
    
    for account_sheet in account_sheets:
        html += frappe.render_template('templates/kontoblaetter/kontoblaetter.html', {'account': account_sheet, 'name': docname})
    
    html += """
        </div>
        </div>
    </body><!-- Administrator --></html>"""
    
    html = frappe.get_print(doctype, docname, html=html)
    
    # create pdf
    pdf = frappe.utils.pdf.get_pdf(html)
    # save and attach pdf
    now = datetime.now()
    ts = "{0:04d}-{1:02d}-{2:02d}".format(now.year, now.month, now.day)
    file_name = "{0}_{1}.pdf".format(ts, docname.replace(" ", "_").replace("/", "_"))
    save_file(file_name, pdf, doctype, docname, is_private=1)
    return
