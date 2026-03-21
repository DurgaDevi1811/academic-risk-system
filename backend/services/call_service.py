from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_SID"),
    os.getenv("TWILIO_AUTH")
)

# Your ngrok/public URL (IMPORTANT)
BASE_URL = "https://mercilessly-lumbar-gregoria.ngrok-free.dev"

def make_call(to_number, message_type):
    try:
        print(f"📞 Calling {to_number}")

        call = client.calls.create(
            url=f"{BASE_URL}/voice?type={message_type}",  # 👈 pass type
            to=to_number,
            from_=os.getenv("TWILIO_PHONE")
        )

        print("✅ Call initiated:", call.sid)
        return call.sid

    except Exception as e:
        print("❌ Call failed:", e)
        return None