from fastapi import FastAPI
import joblib
import numpy as np
import os
import pandas as pd
from xgboost import data
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
@app.get("/predict")
def predict(attendance: float, marks: float, phone: str):
    import pandas as pd

    data = pd.DataFrame([[attendance, marks]], columns=["attendance", "marks"])
    prediction = model.predict(data)[0]

    response = {
        "attendance": attendance,
        "marks": marks,
        "risk": int(prediction)
    }

    # send SMS if at risk
    if prediction == 1:
        message = f"Alert: Student is at risk! Attendance: {attendance}, Marks: {marks}"
        send_sms(phone, message)
        response["alert"] = "SMS Sent"

    return response