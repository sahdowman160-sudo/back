from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from schemas import Insert_Cart_user
import models

router = APIRouter()
@router.post("/insert_cart")
def create_product(product: Insert_Cart_user, db: Session = Depends(get_db)):
    # Get user ID from token
    get_token = get_current_user(product.token_user)
    if not get_token:
        return {"error": "Invalid token"}

    # Create new cart item
    new_product = models.Cart(
        id_product=product.id,  # ID of the product being added
        price=product.price,
        quantity=product.quantity,
        size=product.size,
        token_user=str(get_token["id"])  # تحويله لـ string لو لازم
    )

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    return {
        "message": "✅ Add Product successfully",
        "cart_item": {
            "id": new_product.id,
            "product_id": new_product.id_product,
            "price": new_product.price,
            "quantity": new_product.quantity,
            "size": new_product.size
        }
    }
