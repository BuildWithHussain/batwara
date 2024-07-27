# Copyright (c) 2024, Build With Hussain and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestExpense(FrappeTestCase):
	def test_equal_split_calculation(self):
		# TODO: also create test users before
		test_expense = frappe.get_doc({
			"doctype": "Expense",
			"description": "test expense",
			"paid_by": "friend1@email.com",
			"amount": 200,
			"splits": [
				{
					"user": "friend1@email.com"
				},
				{
					"user": "friend2@email.com"
				}
			]
		}).insert()

		self.assertEqual(test_expense.splits[0].amount, 100)
		self.assertEqual(test_expense.splits[1].amount, 100)


