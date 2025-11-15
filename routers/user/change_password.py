from fastapi import FastAPI, Depends, HTTPException, APIRouter, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from database import SessionLocal
from models import User
from typing import Optional

router = APIRouter()
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# إعدادات JWT
SECRET_KEY = "hello"  # نفس المفتاح المستخدم في users.py
ALGORITHM = "HS256"


# نموذج البيانات
class ChangePasswordData(BaseModel):
    current_password: str
    new_password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# دالة للتحقق من JWT والحصول على المستخدم الحالي
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="غير مصرح: Token مفقود")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        
        if id is None:
            raise HTTPException(status_code=401, detail="Token غير صالح")
        
        user = db.query(User).filter(User.id == id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        
        return user
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token منتهي الصلاحية")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token غير صالح")


# 🔹 تغيير كلمة المرور
@router.post("/change-password")
def change_password(
    data: ChangePasswordData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # التحقق من كلمة المرور الحالية
    if not pwd_context.verify(data.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="كلمة المرور الحالية غير صحيحة")
    
    # التحقق من قوة كلمة المرور الجديدة
    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    
    # التحقق من أن كلمة المرور الجديدة مختلفة عن القديمة
    if pwd_context.verify(data.new_password, current_user.password):
        raise HTTPException(status_code=400, detail="كلمة المرور الجديدة يجب أن تكون مختلفة عن القديمة")
    
    # تحديث كلمة المرور
    hashed_password = pwd_context.hash(data.new_password)
    current_user.password = hashed_password
    db.commit()
    
    return {
        "message": "تم تغيير كلمة المرور بنجاح",
        "status": "success"
    }


# 🔹 endpoint إضافي: الحصول على بيانات المستخدم الحالي
@router.get("/me")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "active": current_user.active
    }