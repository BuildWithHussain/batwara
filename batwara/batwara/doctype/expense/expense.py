# Copyright (c) 2024, Build With Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Expense(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from batwara.batwara.doctype.expense_split.expense_split import ExpenseSplit
		from frappe.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		currency: DF.Link
		date: DF.Date
		description: DF.Data
		notes: DF.SmallText | None
		paid_by: DF.Link
		split_method: DF.Literal["Equally", "Manually", "Percentage"]
		splits: DF.Table[ExpenseSplit]
	# end: auto-generated types

	def before_save(self):
		self.apply_split()

	def apply_split(self):
		if self.split_method == "Equally":
			self.calculate_equal_splits()
		elif self.split_method == "Percentage":
			self.validate_percentage_splits()
			self.calculate_percentage_splits() 
		else:
			# manually
			self.validate_manual_splits()

	def validate_manual_splits(self):
		sum_of_splits = sum(x.amount for x in self.splits)

		if sum_of_splits != self.amount:
			frappe.throw("Sum of splits must be equal to total amount!")

	def calculate_equal_splits(self):
		num_splits = len(self.splits)
		split_amount = self.amount / num_splits

		for s in self.splits:
			s.amount = split_amount
	
	def validate_percentage_splits(self):
		sum_of_percentages = sum(x.percentage for x in self.splits)
		if sum_of_percentages != 100:
			frappe.throw("Sum of percentages must equal 100%!")

	def calculate_percentage_splits(self):
		for s in self.splits:
			s.amount = (s.percentage / 100) * self.amount

	def before_submit(self):
		self.create_ledger_entries()

	def create_ledger_entries(self):
		for split in self.splits:
			if split.user == self.paid_by:
				continue

			le = frappe.new_doc("Split Ledger Entry")
			le.amount = split.amount
			le.currency = split.currency
			le.credit_user = split.user
			le.debit_user = self.paid_by
			le.expense = self.name
			le.insert().submit()

	def after_insert(self):
		self.submit()
