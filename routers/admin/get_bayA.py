from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from models import Bay, Proudect

router = APIRouter()

@router.post("/get_bayA")
def get_all_bay_with_products(db: Session = Depends(get_db)):
    # Join Bay with Proudect using product ID
    results = db.query(Bay, Proudect).join(
        Proudect, Bay.id_product == Proudect.id
    ).all()

    # Format the response to include fields from both tables
    return [
        {
            "id":bay.id,
            "id_product": bay.id_product,
            "token_user": bay.token_user,
            "name": product.name,
            "price": bay.price, 
            "size":bay.size,          # from Bay (price at time of purchase)
            "stute": bay.stute,
            "image": product.image,
            "category": product.category,
            "time": bay.time,
            "loction": bay.loction,
            "way_payment":bay.way_payment,
            "quantity": getattr(bay, "quantity", None)
        }
        for bay, product in results
    ]
