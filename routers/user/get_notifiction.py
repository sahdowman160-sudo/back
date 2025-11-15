from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from models import Notifition

router = APIRouter()

@router.get("/message")
def get_products(db: Session = Depends(get_db)):
    message = db.query(Notifition).all()

    return [
        {
            "name": p.name,
            "message": p.message,
        }
        for p in message
    ]
