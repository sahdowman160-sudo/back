from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Notifition
import models

router = APIRouter()

@router.post("/insert_notfiction")
def create_product(notfiction: Notifition, db: Session = Depends(get_db)):
    # يمكنك هنا حفظ البيانات في قاعدة البيانات
    new_product = models.Notifition(
        name=notfiction.name,
        message=notfiction.message
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "✅ Add message successfully",
    }
