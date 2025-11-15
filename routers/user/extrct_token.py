from fastapi import APIRouter, Depends
from auth import get_current_user
from schemas import Extact
from models import User
from sqlalchemy.orm import Session
import sys
import os
from database import get_db
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
router = APIRouter()

@router.post("/extrct")
def ex(ex:Extact , db: Session = Depends(get_db)):
 get_token= get_current_user(ex.token_user)
 user = db.query(User).filter(User.token_user == ex.token_user).first()
 
 return {"info": get_token, "status": "success" }

