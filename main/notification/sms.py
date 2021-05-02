from twilio.rest import Client
from decouple import config

account_sid = config("ACCOUNT_SID")
auth_token = config("AUTH_TOKEN")


class SMSNotify:
    def __init__(self):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def message(self, store, error=False):
        if error:
            body = store + " bot had an error."
        else:
            body = store + " has what you are looking for."
        message = self.client.messages.create(
            messaging_service_sid=config("MESSAGE_SID"),
            body=body,
            to=config("PHONE_TO")
        )

        print("Sent message: " + message.sid)
