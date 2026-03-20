from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_SID"),
    os.getenv("TWILIO_AUTH")
)

def send_sms(to_number, message):
    try:
        print(f"📩 Sending SMS to {to_number}")

        msg = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE"),
            to=to_number
        )

        print("✅ SMS Sent:", msg.sid)
        return msg.sid

    except Exception as e:
        print("❌ SMS Failed:", e)
        return None