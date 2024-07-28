import frappe
from twilio.rest import Client


def get_twilio_client():
	batwara_settings = frappe.get_doc("Batwara Settings")
	account_sid = batwara_settings.twilio_account_sid
	auth_token = batwara_settings.get_password("twilio_auth_token")

	return Client(account_sid, auth_token)

def send_text_message(message_body: str, to: str, from_: str):
	client = get_twilio_client()
	return client.messages.create(
		from_=from_,
		body=message_body,
		to=to
	)
