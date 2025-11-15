from pydantic import BaseModel ,EmailStr
from models import User
from database import get_db
from sqlalchemy.orm import Session
from fastapi import  Depends
from functools import lru_cache
from typing import List, Optional
class Extact(BaseModel):
    token_user:str
class Point_user(BaseModel):
    token:str
class Delete_product(BaseModel):
    id:int
class Search(BaseModel):
    name:str 
class Select(BaseModel):
    id:str 
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    status: str
    hi:str
class Send_email(BaseModel):
    email: str
    message: str
    name: str
    subject:str
class Change_stute(BaseModel):
    id:int
    id_product: str
    stute: str
    token_user: str
class ProductCreate(BaseModel):
    name: str
    caption: str
    price: float
    image: Optional[List[str]] = None  # قائمة روابط الصور أو أسماء الملفات

    class Config:
        orm_mode = True
class TokenRequest(BaseModel):
    token: str
class sendemail(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class Cart_user(BaseModel):
    token_user: str 
class Insert_Cart_user(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    size: str
    token_user: str   
class Cart_check(BaseModel):
    id: int  # Product ID
    token_user: str
class Delet_cart(BaseModel):
    id: int  # Product ID
    token_user: str
class Bay_user(BaseModel):
    id_product: str
    loction:str
    price: float
    quantity: str
    size:str
    stute:str
    time:str
    token_user:str
    phone1: str
    phone2: str
    way_payment:str
class Cancel_order(BaseModel):
    id_product: str
    stute:str
    token_user:str
class Try_on(BaseModel):
    clothes: str
    model:str
class Bay_get(BaseModel):
    token_user: str
class like_user(BaseModel):
    id: int
    token_user:str

class Cart_user_page(BaseModel):
    token_user:str
class not_user_page(BaseModel):
    token_user:str
class like_user_page(BaseModel):
    token_user:str
class Notifition(BaseModel):
    name: str
    message:str
class RegisterData(BaseModel):
    email: EmailStr
    password: str


class VerifyCodeData(BaseModel):
    email: EmailStr
    verificationCode: int

class Settings:
    def __init__(self, usernames, passwords):
        print("📥 Loading settings ... (مرة واحدة بس)")
        self.app_name = usernames           # usernames list
        self.admin_email = passwords        # passwords list
        self.items_per_user = len(usernames)

def load_settings(db: Session):
    usernames = [u[0] for u in db.query(User.username).all()]
    passwords = [p[0] for p in db.query(User.password).all()]
    return Settings(usernames, passwords)
    
@lru_cache()
def get_settings(db: Session = Depends(get_db)):
    return load_settings(db)
