from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
import models
router = APIRouter()
@router.get("/addverise")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Addvertise).all()
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
            "image":p.image, 
        }
        for p in products
    ]
