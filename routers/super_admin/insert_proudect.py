from fastapi import APIRouter, Depends
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from schemas import ProductCreate
import models

router = APIRouter()

@router.post("/insert_proudect")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # يمكنك هنا حفظ البيانات في قاعدة البيانات
    new_product = models.Proudect(
        name=product.name,
        price=product.price,
        caption=product.caption,
        image=str(product.image)  # نحول المصفوفة إلى نص إذا العمود نصي
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "✅ Product created successfully",
        "data": new_product
    }
