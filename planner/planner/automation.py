# -*- coding: utf-8 -*-
# Copyright (c) 2023, libracore AG and contributors
# For license information, please see license.txt

import frappe

def extend_and_submit_journal_entry(self, event):

	#return if not auto-repeat
	if not self.auto_repeat:
		return
	#get user-remark from origin document
	origin = frappe.db.sql("""
		SELECT `tabJournal Entry`.`user_remark`
		FROM `tabAuto Repeat`
		LEFT JOIN `tabJournal Entry` ON `tabAuto Repeat`.`reference_document` = `tabJournal Entry`.`name`
		WHERE `tabJournal Entry`.`auto_repeat` = '{auto}'
	""".format(auto=self.auto_repeat), as_dict=True)
	
	#update user-remark on actual document	
	update_remark = frappe.db.sql("""UPDATE `tabJournal Entry` SET `user_remark` = '{remark}' WHERE `name` ='{name}'""".format(remark=origin[0]['user_remark'], name=self.name), as_list=True)
	
	#auto-submit document
	journal_entry = frappe.get_doc("Journal Entry", self.name)
	journal_entry.submit()

	return
