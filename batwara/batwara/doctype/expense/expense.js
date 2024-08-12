// Copyright (c) 2024, Build With Hussain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense", {
	onload(frm) {
		frm.set_query("paid_by", function () {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
});
