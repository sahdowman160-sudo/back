from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import like_user_page
from auth import get_current_user
from models import Like, Proudect  # Added Proudect import

router = APIRouter()

@router.post("/like")
def get_products(data: like_user_page, db: Session = Depends(get_db)):
    # استخرج الـ user من التوكن
    get_token = get_current_user(data.token_user)
    
    # join بين Like و Proudect
    results = db.query(Like, Proudect).join(
        Proudect, Like.product_id == Proudect.id
    ).filter(
        Like.token_user == str(get_token["id"])
    ).all()
    
    # اعادة البيانات بشكل منسق
    return [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "caption": product.caption,
            "category":product.category,
            "rating":product.rating,
            "reviews":product.reviews,
            "originalPrice":product.originalPrice,
            "image":product.image, 
        }
        for like, product in results
    ]