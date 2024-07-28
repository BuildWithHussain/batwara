# Copyright (c) 2024, Build With Hussain and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BatwaraSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		msg91_authkey: DF.Password | None
		twilio_account_sid: DF.Data | None
		twilio_auth_token: DF.Password | None
		twilio_phone_number: DF.Data | None
		twilio_service_id: DF.Data | None
	# end: auto-generated types

	pass
