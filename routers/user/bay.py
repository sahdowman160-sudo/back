from fastapi import APIRouter, Depends
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from schemas import Bay_user
from datetime import datetime
import models

router = APIRouter()

@router.post("/Bay")
def create_buy(product: Bay_user, db: Session = Depends(get_db)):
    # تحقق من المستخدم عبر التوكن
    get_token = get_current_user(product.token_user)

    # تحديث النقاط (إضافة 10 نقاط عند كل عملية شراء)
    user_point = db.query(models.Point).filter(models.Point.token_user == get_token["id"]).first()
    if user_point:
        user_point.point += 10
    else:
        user_point = models.Point(point=10, token_user=get_token["id"])
        db.add(user_point)

    # إنشاء عملية شراء جديدة
    new_buy = models.Bay(
        id_product=product.id_product,
        price=product.price,
        quantity=product.quantity,
        size=product.size,
        stute=product.stute,
        time=datetime.utcnow(),  # الوقت الحالي بدل الوقت المرسل من المستخدم
        way_payment=product.way_payment,
        loction=product.loction,
        phone1=product.phone1,
        phone2=product.phone2,
        token_user=get_token["id"]
    )

    db.add(new_buy)
    db.commit()
    db.refresh(new_buy)
    db.refresh(user_point)

    return {"message": "✅ Purchase created successfully", "buy_id": new_buy.id}
