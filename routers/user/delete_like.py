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

@router.post("/delete_like")
def delete_like(like: like_user, db: Session = Depends(get_db)):
    # Get the current user from token
    get_token = get_current_user(like.token_user)
    
    # Check if the product is liked by this user
    existing_like = db.query(models.Like).filter(
        models.Like.product_id == like.id,
        models.Like.token_user == get_token["id"]
    ).first()
    
    # If not liked, return that it's not in wishlist
    if not existing_like:
        return {
            "status": "not_found",
            "message": "Product is not in your wishlist"
        }
    
    # If liked, remove it from the database
    db.delete(existing_like)
    db.commit()
    
    return {
        "status": "success",
        "message": "Product removed from wishlist successfully"
    }