from fastapi import FastAPI, Depends, HTTPException , APIRouter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from email.message import EmailMessage
import smtplib, random, jwt, os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from database import SessionLocal ,get_db
from models import User  # اسم الجدول عندك user
from schemas import Send_email
router = APIRouter()

@router.post("/send_email")
def register(user_data: Send_email, db: Session = Depends(get_db)):

        # إرسال الإيميل
        msg = EmailMessage()
        msg["Subject"] = user_data.subject
        msg["From"] = user_data.name
        msg["To"] = "jmh199635@gmail.com"
        msg.set_content(user_data.message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("jmh199635@gmail.com", "wcoj apaw mbur ixka")
            smtp.send_message(msg)

        return {"status": "success" , "email":user_data.email}


