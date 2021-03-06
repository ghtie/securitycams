import os
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)


def send_message(message):
    """
    Send an SMS text message through twillio
    :param message: string message to send
    """
    client.api.account.messages.create(
        to="phone number to receive messages",
        from_="twilio issued phone number",
        body=message)
