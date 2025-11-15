from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from schemas import like_user
import models

router = APIRouter()

@router.post("/insert_like")
def create_product(like: like_user, db: Session = Depends(get_db)):
    # Get the current user from token
    get_token = get_current_user(like.token_user)
    
    # If not liked, add it to the database
    new_product = models.Like(
        product_id=like.id,
        token_user=get_token["id"]
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {
        "status": "success",
        "message": "Product added to wishlist successfully"
    }