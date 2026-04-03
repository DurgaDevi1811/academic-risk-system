from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import pandas as pd
from sqlalchemy.orm import Session
from database.db import init_db, get_db, Student, Alert
from services.sms_service import send_sms
from services.call_service import make_call 

app = FastAPI()

# -----------------------------
# CORS SETTINGS (For Frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# INIT DATABASE
# -----------------------------
init_db()

# -----------------------------
# LOAD MODEL
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "federated", "global_model.pkl")
if not os.path.exists(model_path):
    model_path = os.path.join(BASE_DIR, "models", "student_risk_model.pkl")

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# ... (Previous endpoints)

@app.post("/predict")
def predict(request: dict, db: Session = Depends(get_db)):
    try:
        student_name = request.get("student_name")
        attendance = float(request.get("attendance", 0))
        marks = float(request.get("marks", 0))
        phone = request.get("phone")

        # ML prediction
        prediction = 0
        if model:
            df = pd.DataFrame([[attendance, marks]], columns=["attendance", "marks"])
            prediction = int(model.predict(df)[0])
        else:
            if attendance < 50 or marks < 40:
                prediction = 1

        # Send Alerts
        sms_sid = None
        call_sid = None
        alert_type = None
        
        if attendance < 50 and marks < 40:
            alert_type = "both"
        elif attendance < 50:
            alert_type = "attendance"
        elif marks < 40:
            alert_type = "marks"

        if alert_type:
            msg = f"Alert: {student_name} risk detected ({alert_type})."
            sms_sid = send_sms(phone, msg)
            call_sid = make_call(phone, f"{alert_type}|{student_name}")

        # SAVE TO STUDENTS TABLE
        student = Student(
            name=student_name,
            mobile=phone,
            attendance=attendance,
            marks=marks,
            roll_no="TBD"
        )
        db.add(student)
        db.commit()

        # SAVE TO ALERTS TABLE
        new_alert = Alert(
            call_sid=str(call_sid) if call_sid else None,
            sms_sid=str(sms_sid) if sms_sid else None,
            call_status="SENT" if call_sid else "NONE",
            sms_status="SENT" if sms_sid else "NONE"
        )
        db.add(new_alert)
        db.commit()

        return {"status": "Success", "risk": prediction}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # Fetch from dynamic student table
    students = db.query(Student).order_by(Student.id.desc()).limit(20).all()
    # We can map them to display risk based on logic since they don't have a 'risk' column
    result = []
    for s in students:
        risk = 1 if (s.attendance < 50 or s.marks < 40) else 0
        result.append({
            "student_name": s.name,
            "attendance": s.attendance,
            "marks": s.marks,
            "risk": risk
        })
    return result

@app.api_route("/voice", methods=["GET", "POST"])
def voice(request: Request):
    data = request.query_params.get("type")

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

    return Response(content=xml_response.strip(), media_type="application/xml")
