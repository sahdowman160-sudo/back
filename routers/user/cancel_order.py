from fastapi import APIRouter, Depends
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
import models

router = APIRouter()

@router.post("/cancel_order")
def edit_bay_status(data: dict, db: Session = Depends(get_db)):
    """
    تعديل حالة عملية شراء بناءً على id_product و token_user
    """
    # التحقق من المستخدم عبر التوكن
    get_token = get_current_user(data["token_user"])

    # البحث عن الطلب المطلوب تعديله
    bay_item = db.query(models.Bay).filter(
        models.Bay.token_user == str(get_token["id"]),
        models.Bay.id_product == data["id_product"],
        models.Bay.id == data["id"]
    ).first()

    if not bay_item:
        return {"error": "❌ No order found for this user or product."}

    # تعديل الحالة
    bay_item.stute = data["stute"]
    db.commit()
    db.refresh(bay_item)

    return {"message": "✅ Status updated successfully", "new_stute": bay_item.stute}
