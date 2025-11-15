from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Cart_check
from auth import get_current_user
from models import Cart

router = APIRouter()

@router.post("/check")
def get_products(data: Cart_check, db: Session = Depends(get_db)):
    get_token= get_current_user(data.token_user)
    products = db.query(Cart).filter((Cart.token_user == get_token["id"]) & (Cart.id_product == data.id)).all()

    if products :
     return {"add":"found"}
    else:
     return {"add":"notFound"} 

    