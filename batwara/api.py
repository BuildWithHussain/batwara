import frappe


@frappe.whitelist()
def get_summary_for_session_user():
	user = frappe.session.user
	return get_summary_for_user(user)


def get_summary_for_user(user: str) -> list:
	owed_to_user = frappe.get_all(
		"Split Ledger Entry",
		fields=[
			"SUM(amount) AS amount",
			"credit_user",
			"currency",
		],  # assuming all transactions in same currency
		filters={"debit_user": user},
		group_by="credit_user",
	)
	owed_to_user_dict = {}
	for record in owed_to_user:
		owed_to_user_dict[record["credit_user"]] = {
			"amount": record["amount"],
			"currency": record["currency"],
		}

	user_owes = frappe.get_all(
		"Split Ledger Entry",
		fields=[
			"SUM(amount) AS amount",
			"debit_user",
			"currency",
		],  # assuming all transactions in same currency
		filters={"credit_user": user},
		group_by="debit_user",
	)
	user_owes_dict = {}
	for record in user_owes:
		user_owes_dict[record["debit_user"]] = {
			"amount": record["amount"],
			"currency": record["currency"],
		}

	unique_friends = set(owed_to_user_dict.keys()).union(set(user_owes_dict.keys()))

	summary = {}
	for friend in unique_friends:
		if friend in owed_to_user_dict and friend in user_owes_dict:
			owed_to_user = owed_to_user_dict[friend]["amount"] - user_owes_dict[friend]["amount"]

			if owed_to_user < 0:
				summary[friend] = {"net_amount": owed_to_user, "type": "to_give"}
			elif owed_to_user > 0:
				summary[friend] = {"net_amount": owed_to_user, "type": "to_receive"}
			else:
				summary[friend] = {"net_amount": owed_to_user, "type": "even"}
		elif friend in owed_to_user_dict:
			amount = owed_to_user_dict[friend]["amount"]
			summary[friend] = {"net_amount": amount, "type": "to_receive"}
		else:
			amount = user_owes_dict[friend]["amount"]
			summary[friend] = {"net_amount": amount, "type": "to_send"}

	return summary
