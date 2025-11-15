from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import Delete_product
from auth import get_current_user
from models import Proudect

router = APIRouter()

@router.post("/Delet_Product")
def get_products(data: Delete_product, db: Session = Depends(get_db)):
    new_product=db.query(Proudect).filter((Proudect.id == data.id)).delete(synchronize_session=False)
    db.commit()  # Don't forget to commit the transaction
    return {"pro": new_product }


    