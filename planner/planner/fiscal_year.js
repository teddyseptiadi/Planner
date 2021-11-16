frappe.ui.form.on('Fiscal Year', {
	refresh(frm) {
        frm.add_custom_button(__("Kontenblätter als PDF erzeugen"), function() {
            pdf_all(frm);
        });
	}
});

function pdf_all(frm) {
    frappe.call({
        "method": "planner.planner.pdf.enqueue_create_pdf",
        "args": {
            "doctype": frm.doc.doctype,
            "docname": frm.doc.name
        },
        "callback": function(response) {
            frappe.msgprint( __("Der PDF-Auftrag wurde aufgegeben. Das fertige PDF wird in kürze als Anhang verfügbar sein.") );
        }
    });
}
