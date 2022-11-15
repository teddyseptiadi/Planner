# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.data import date_diff

def execute(filters=None):
    columns = [
        "Buchung:Link/Booking:150",
        "Gebuchte Tage:Int",
        "Tage in Auftrag:Int",
        "Monate in Auftrag:Int",
        "Status"
    ]
    data = check_booking_orders(filters)
    return columns, data

def check_booking_orders(filters):
    data = []
    
    bookings = frappe.db.sql("""SELECT `name`, `end_date`, `start_date` FROM `tabBooking` WHERE `booking_status` = 'Booked' AND `start_date` >= '{start}'""".format(start=filters.from_date), as_dict=True)
    
    for booking in bookings:
        mietdauer = date_diff(booking.end_date, booking.start_date) + 1
        orders = frappe.db.sql("""SELECT `name` FROM `tabSales Order` WHERE `booking` = '{booking}' AND `docstatus` != 2""".format(booking=booking.name), as_dict=True)
        tage = 0
        monate = 0
        
        for order in orders:
            o = frappe.get_doc("Sales Order", order.name)
            for item in o.items:
                if item.item_code == 'Miete 3.7 Tag':
                    tage += item.qty
                elif item.item_code in ('Miete 3.7 Mt', 'Miete mt'):
                    monate += item.qty
        tage_max = (monate * 31) + tage
        tage_min = (monate * 30) + tage
        
        if mietdauer >= tage_min and mietdauer <= tage_max:
            result = 'OK'
            if filters.failed != 1:
                _data = []
                _data.append(booking.name)
                _data.append(mietdauer)
                _data.append(int(tage))
                _data.append(int(monate))
                _data.append(result)
                data.append(_data)
        else:
            abweichung_min = round(100 - ((100 / mietdauer) * tage_min), 2)
            abweichung_max = round(100 - ((100 / mietdauer) * tage_max), 2)
            if mietdauer > tage_max:
                abweichung = mietdauer - tage_max
            else:
                abweichung = tage_min - mietdauer
            result = 'Failed --> Minimum Differenz: {0} Tag(e)'.format(abweichung)
            _data = []
            _data.append(booking.name)
            _data.append(mietdauer)
            _data.append(int(tage))
            _data.append(int(monate))
            _data.append(result)
            data.append(_data)
        
    return data
