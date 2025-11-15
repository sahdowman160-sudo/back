from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Search
from models import Proudect
router = APIRouter()
@router.post("/search")
def get_products(search:Search , db: Session = Depends(get_db)):
    products = db.query(Proudect).filter(Proudect.name == search.name).all()
    if products :
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
    else:
        return{"data":"This proudect not found"}
    
