from fastapi import APIRouter, Depends, HTTPException, status
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from schemas import LoginRequest, TokenResponse
from models import User
from database import get_db
from auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if user.role == "user": 
       token = create_access_token({"id":user.id})
       user.token_user = token
       db.commit()
       return {"access_token": token, "status": "success" ,"token_type": "bearer" , "hi": "b"}
    if user.role == "admin":
       token = create_access_token({"id":user.id})
       user.token_user = token
       db.commit()
       return {"access_token": token, "status": "success" ,"token_type": "bearer" , "hi": "m"}
    if user.role == "super":
       token = create_access_token({"id":user.id})
       user.token_user = token
       db.commit()
       return {"access_token": token, "status": "success" ,"token_type": "bearer" , "hi": "s"}
