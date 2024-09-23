# Copyright (c) 2024, Build With Hussain and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExpenseSplit(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		currency: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Float
		user: DF.Link
	# end: auto-generated types
	pass
