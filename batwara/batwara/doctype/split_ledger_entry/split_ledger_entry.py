# Copyright (c) 2024, Build With Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SplitLedgerEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		credit_user: DF.Link
		currency: DF.Link | None
		debit_user: DF.Link
		expense: DF.Link | None
		is_settlement: DF.Check
	# end: auto-generated types

	def validate(self):
		self.validate_credit_and_debit_user_different()

	def validate_credit_and_debit_user_different(self):
		if self.credit_user == self.debit_user:
			frappe.throw("You can't pay yourself!")
