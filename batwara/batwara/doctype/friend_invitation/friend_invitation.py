# Copyright (c) 2024, Build With Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from batwara.utils import send_text_message


class FriendInvitation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		invited_by: DF.Link
		invitee_name: DF.Data
		invitee_phone: DF.Data
		status: DF.Literal["Not Sent", "Pending", "Accepted", "Rejected"]
	# end: auto-generated types

	def after_insert(self):
		self.send_invite()

	def send_invite(self):
		invited_by = frappe.db.get_value("User", self.invited_by, "full_name")
		invitation_link = f"https://{frappe.local.site}/frontend/login?code={self.name}"

		message = f"""
Hey {self.invitee_name}! {invited_by} has invited you to join their friend circle on batwara.app: {invitation_link}
"""
		if not frappe.conf.developer_mode:
			send_text_message(message, self.invitee_phone)
		else:
			print(message)

		self.db_set("status", "Pending")
