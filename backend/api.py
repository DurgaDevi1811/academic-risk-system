from unittest.mock import call

from fastapi import FastAPI
import joblib
import os
import pandas as pd
from services.sms_service import send_sms
from fastapi import Request
from fastapi.responses import Response
from services.call_service import make_call 
app = FastAPI()

# -----------------------------
# LOAD MODEL
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "federated", "global_model.pkl")

model = joblib.load(model_path)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.get("/")
def home():
    return {"message": "Academic Risk Prediction API Running"}

# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.post("/predict")
def predict(request: dict):
    try:
        student_name = request["student_name"]
        attendance = request["attendance"]
        marks = request["marks"]
        phone = request["phone"]

        # thresholds (same as preprocessing)
        ATTENDANCE_THRESHOLD = 50
        MARKS_THRESHOLD = 40

        # ML prediction (optional but kept)
        df = pd.DataFrame([[attendance, marks]], columns=["attendance", "marks"])
        prediction = model.predict(df)[0]

        response = {
            "attendance": attendance,
            "marks": marks,
            "risk": int(prediction)
        }

        # -----------------------------
        # RULE-BASED ALERT SYSTEM
        # -----------------------------
        message = None
        call_type = None
        if attendance < ATTENDANCE_THRESHOLD and marks < MARKS_THRESHOLD:
            message = f"Alert: {student_name} has low attendance ({attendance}) and low marks ({marks}). Immediate attention required."
            call_type = f"both|{student_name}"
        elif attendance < ATTENDANCE_THRESHOLD:
            message = f"Alert: {student_name} has low attendance ({attendance}). Please take action."
            call_type = f"attendance|{student_name}"
        elif marks < MARKS_THRESHOLD:
            message = f"Alert: {student_name}'s marks ({marks}) are below 40%. Please take action."
            call_type = f"marks|{student_name}"
        # send alerts
        if message:
            send_sms(phone, message)
            make_call(phone, call_type)
            response["alert"] = "SMS + CALL Sent"
            response["message"] = message
        else:
            response["message"] = "Student is Safe"
        return response
    except Exception as e:
        return {"error": str(e)}

@app.post("/voice")
def voice(request: Request):
    data = request.query_params.get("data")

    if data:
        parts = data.split("|")
        msg_type = parts[0]
        student_name = parts[1]
    else:
        msg_type = None
        student_name = "విద్యార్థి"

    if msg_type == "marks":
        telugu_msg = f"ఇది కళాశాల నుండి ఆటోమేటిక్ అలర్ట్. విద్యార్థి {student_name} యొక్క మార్కులు నలభై శాతం కంటే తక్కువగా ఉన్నాయి."

    elif msg_type == "attendance":
        telugu_msg = f"ఇది కళాశాల నుండి ఆటోమేటిక్ అలర్ట్. విద్యార్థి {student_name} యొక్క హాజరు తక్కువగా ఉంది."

    elif msg_type == "both":
        telugu_msg = f"ఇది కళాశాల నుండి ఆటోమేటిక్ అలర్ట్. విద్యార్థి {student_name} యొక్క హాజరు మరియు మార్కులు రెండూ తక్కువగా ఉన్నాయి."

    else:
        telugu_msg = "విద్యార్థి సమాచారం అందుబాటులో లేదు."

    xml_response = f"""
    <Response>
        <Say language="te-IN" voice="alice">
            {telugu_msg}
        </Say>
    </Response>
    """

    return Response(content=xml_response, media_type="application/xml")