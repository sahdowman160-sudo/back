from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Delet_cart
from auth import get_current_user
from models import Cart

router = APIRouter()

@router.post("/Delet_cart")
def get_products(data: Delet_cart, db: Session = Depends(get_db)):
    get_token= get_current_user(data.token_user)
    new_product=db.query(Cart).filter((Cart.token_user == get_token["id"]) & (Cart.id_product == data.id)).delete(synchronize_session=False)
    db.commit()  # Don't forget to commit the transaction
    return {"pro": new_product }


    