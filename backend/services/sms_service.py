from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_SID"),
    os.getenv("TWILIO_AUTH")
)

def send_sms(to_number, message):
    return client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_PHONE"),
        to=to_number
    )