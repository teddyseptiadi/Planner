import frappe
from frappe import _

def execute():
    print("Start Reset")
    try:
        apps = frappe.db.sql("""SELECT `name` FROM `tabAppartment` WHERE `planned_until` IS NOT NULL""", as_dict=True)
        for app in apps:
            books = frappe.db.sql("""SELECT `start_date` FROM `tabBooking` WHERE `appartment` = '{0}' AND `booking_status` = 'Service-Cleaning' ORDER BY `start_date` DESC LIMIT 1""".format(app.name), as_dict=True)
            if len(books) > 0:
                frappe.db.sql("""UPDATE `tabAppartment` SET `planned_until` = '{0}' WHERE `name` = '{1}'""".format(books[0].start_date, app.name), as_list=True)
        print("Done")
    except Exception as err:
        print("failed: {0}".format(err))
    return
