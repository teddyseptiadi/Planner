# -*- coding: utf-8 -*-
# Copyright (c) 2023, libracore AG and contributors
# For license information, please see license.txt

import frappe

def extend_and_submit_journal_entry(self, event):

	#return if not auto-repeat
	if not self.auto_repeat:
		return
	#get name of origin document and user-remark from origin document
	origin = frappe.db.get_value("Auto Repeat", {"Name": self.auto_repeat}, "reference_document")
	remark = frappe.db.get_value("Journal Entry", {"Name": origin}, "user_remark")
	
	#get, update, save and submit document
	journal_entry = frappe.get_doc("Journal Entry", self.name)
	journal_entry.user_remark = remark
	journal_entry.save()
	journal_entry.submit()

	return
