from fastapi import APIRouter, Depends, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from models import User
from schemas import LoginRequest
from database import get_db
from auth import get_password_hash

router = APIRouter()

@router.post("/registeradmin")
def register(user: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token({"sub": user.email, "role": user.role , "id":user.id})
    user.token_user = token
    db.commit()
    return {"access_token": token, "token_type": "bearer"}
