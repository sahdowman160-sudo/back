from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Bay_get
from auth import get_current_user
from models import Bay, Proudect  # Added Proudect import

router = APIRouter()

@router.post("/get_bay")
def get_products(data: Bay_get, db: Session = Depends(get_db)):
    # استخرج الـ user من التوكن
    get_token = get_current_user(data.token_user)
    
    # join بين Like و Proudect
    results = db.query(Bay, Proudect).join(
        Proudect, Bay.id_product == Proudect.id
    ).filter(
        Bay.token_user == str(get_token["id"])
    ).all()
    
    # اعادة البيانات بشكل منسق
    return [
        {
            "id_product": Bay.id_product,
            "token_user": Bay.token_user,
            "id": Bay.id,
            "name": product.name,
            "price": Bay.price,
            "stute": Bay.stute,
            "image": product.image,
            "time": Bay.time,
            "quantity": Bay.quantity,
            "name": product.name,
        }
        for Bay, product in results
    ]