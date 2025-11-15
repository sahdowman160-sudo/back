from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from schemas import Cart_user
from auth import get_current_user
from models import Cart, Proudect  # Product class

router = APIRouter()

@router.post("/cart_user")
def get_products(data: Cart_user, db: Session = Depends(get_db)):
    # استخرج الـ user من التوكن
    get_token = get_current_user(data.token_user)
    
    # join بين Cart و Proudect
    results = db.query(Cart, Proudect).join(
        Proudect, Cart.id_product == Proudect.id
    ).filter(
        (Cart.token_user == str(get_token["id"])) 
    ).all()
    
    # اعادة البيانات بشكل منسق
    return [
        {
            "cart_id": cart.id_product,
            "quantity": cart.quantity,
            "size": cart.size,
            "originalPrice": product.originalPrice,
            "image": product.image,
            "price": product.price,
            "name": product.name,
        }
        for cart, product in results
    ]
