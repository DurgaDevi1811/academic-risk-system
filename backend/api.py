from fastapi import FastAPI
import joblib
import os
import pandas as pd
from services.sms_service import send_sms

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

        if attendance < ATTENDANCE_THRESHOLD and marks < MARKS_THRESHOLD:
            message = f"⚠️ Student at HIGH RISK!\nLow Attendance ({attendance}) and Low Marks ({marks})"

        elif attendance < ATTENDANCE_THRESHOLD:
            message = f"⚠️ Low Attendance Alert!\nAttendance: {attendance}"

        elif marks < MARKS_THRESHOLD:
            message = f"⚠️ Low Marks Alert!\nMarks: {marks}"

        # send SMS only if any issue
        if message:
            send_sms(phone, message)
            response["alert"] = "SMS Sent"
            response["message"] = message
        else:
            response["message"] = "Student is Safe"

        return response

    except Exception as e:
        return {"error": str(e)}