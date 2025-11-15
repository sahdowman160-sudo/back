from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
import models
router = APIRouter()
@router.post("/count_cart")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Cart).all()
    return {"count": len(products)}