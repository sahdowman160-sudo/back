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
from database import SessionLocal
from models import User  # اسم الجدول عندك user
from schemas import RegisterData,VerifyCodeData
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# إعدادات JWT
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# بيانات الإيميل
sender_email = "jmh199635@gmail.com"
sender_password = "wcoj apaw mbur ixka"  # خذ باسورد تطبيق من Gmail (App Password)


# نماذج الإدخال

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# دالة لتوليد JWT
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# 🔹 تسجيل مستخدم جديد
@router.post("/register")
def register(user_data: RegisterData, db: Session = Depends(get_db)):
    try:
        random_number = random.randint(100000, 999999)
        existing_user = db.query(User).filter(User.email == user_data.email).first()

        hashed_password = pwd_context.hash(user_data.password)

        if existing_user:
            if existing_user.active == 0:
                existing_user.code = random_number
                existing_user.password = hashed_password
                db.commit()
            else:
                raise HTTPException(status_code=400, detail="الحساب موجود ومفعّل مسبقًا")
        else:
            new_user = User(
                email=user_data.email,
                password=hashed_password,
                role="user",
                code=random_number,
                active=0,
            )
            db.add(new_user)
            db.commit()

        # إرسال الإيميل
        msg = EmailMessage()
        msg["Subject"] = "رمز التحقق من VEMS Store"
        msg["From"] = "VEMS Store"
        msg["To"] = user_data.email
        msg.set_content(f"رمز التحقق الخاص بك هو:\n\n{random_number}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return {"message": "تم إرسال كود التحقق إلى البريد الإلكتروني", "status": "success" , "email":user_data.email }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="الإيميل مسجل مسبقًا")


# 🔹 تفعيل الحساب عبر كود التحقق
@router.post("/verify")
def verify_code(data: VerifyCodeData, db: Session = Depends(get_db)):
    user_record = db.query(User).filter(User.email == data.email).first()

    if not user_record:
        raise HTTPException(status_code=404, detail="الحساب غير موجود")

    if user_record.code == data.verificationCode:
        user = db.query(User).filter(User.email == data.email).first()
        user_record.active = 1
        token = create_access_token({"sub": data.email , "role": user.role , "id":user.id})
        user_record.token_user=token
        db.commit()

        
        return {"message": "تم التحقق من الحساب بنجاح", "token": token, "status": "success"}

    else:
        raise HTTPException(status_code=400, detail="رمز تحقق غير صحيح")


