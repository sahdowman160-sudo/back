from fastapi import FastAPI, Depends, HTTPException, APIRouter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from database import SessionLocal
from models import User
from schemas import RegisterData

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Settings
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pydantic Model for Super Admin Registration
class SuperAdminRegisterData(BaseModel):
    email: str
    password: str
    role: str  # "admin" or "superadmin"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to generate JWT
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Register Super Admin or Admin (No verification needed)
@router.post("/register-super-admin")
def register_super_admin(user_data: SuperAdminRegisterData, db: Session = Depends(get_db)):
    try:
        # Validate role
        if user_data.role not in ["admin", "super"]:
            raise HTTPException(status_code=400, detail="الدور يجب أن يكون admin أو superadmin")

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="الحساب موجود مسبقًا")

        # Hash password
        hashed_password = pwd_context.hash(user_data.password)

        # Create new admin/superadmin user
        new_user = User(
            email=user_data.email,
            password=hashed_password,
            role=user_data.role,
            code=None,  # No verification code needed
            active=1,   # Active immediately
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Generate token
        token = create_access_token({
            "sub": new_user.email,
            "role": new_user.role,
            "id": new_user.id
        })

        # Save token to user record
        new_user.token_user = token
        db.commit()

        return {
            "message": "تم إنشاء الحساب بنجاح",
            "status": "success",
            "token": token,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "role": new_user.role
            }
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="الإيميل مسجل مسبقًا")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))