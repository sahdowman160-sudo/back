from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Select
from models import Proudect
router = APIRouter()
@router.post("/select")
def get_products(select:Select , db: Session = Depends(get_db)):
    products = db.query(Proudect).filter(Proudect.id == select.id).all()

    return [
     {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "caption": p.caption,
            "category":p.category,
            "rating":p.rating,
            "reviews":p.reviews,
            "originalPrice":p.originalPrice,
            "image": p.image,
     }
    for p in products
      ]

    
