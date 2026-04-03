from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Connection Details - Priority to .env, otherwise defaults
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "student_alert")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    roll_no = Column(String(20))
    name = Column(String(100))
    mobile = Column(String(15))
    attendance = Column(Float)
    marks = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    call_sid = Column(String(50))
    sms_sid = Column(String(50))
    call_status = Column(String(20), default="PENDING")
    sms_status = Column(String(20), default="PENDING")
    ack_received = Column(Boolean, default=False)
    # student_id = Column(Integer, ForeignKey("students.id")) # Optional: adding relation if needed

class AlertSchedule(Base):
    __tablename__ = "alert_schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    schedule_time = Column(Time)
    max_students = Column(Integer)
    status = Column(String(20), default="pending")

class CallResponse(Base):
    __tablename__ = "call_responses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer)
    call_sid = Column(String(100))
    response = Column(String(50))
    response_time = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    try:
        # We don't necessarily want to recreate tables if they exist, 
        # but create_all will only create those that don't exist.
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing DB: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
