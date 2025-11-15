from fastapi import APIRouter, Depends, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import Bay
from schemas import Change_stute  # you can make a new schema if needed

router = APIRouter()


@router.post("/update_bay_stute")
def update_bay_stute(data: Change_stute, db: Session = Depends(get_db)):
  

    # Verify user from token
  

    # Find the matching Bay record
    bay_item = db.query(Bay).filter((Bay.token_user == data.token_user) & (Bay.id_product == data.id_product) & (Bay.id == data.id)).first()

    if not bay_item:
        raise HTTPException(status_code=404, detail="Order not found for this user")

    # Update status
    bay_item.stute = data.stute
    db.commit()
    db.refresh(bay_item)

    return {
        "message": "Status updated successfully",
        "id_product": bay_item.id_product,
        "new_stute": bay_item.stute,
        "bay":bay_item
    }
