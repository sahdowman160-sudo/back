from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import get_db
from schemas import Point_user
from auth import get_current_user
from models import Point

router = APIRouter()

@router.post("/points")
def get_user_points(data: Point_user, db: Session = Depends(get_db)):
    # extract user from token
    user_id = get_current_user(data.token)

    # get all points for that user
    results = db.query(Point).filter(Point.token_user == user_id["id"]).all()

    if not results:
        raise HTTPException(status_code=404, detail="No points found for this user")

    # format response
    return [
        {
            "point_id": point.id,
            "points": point.point,
            "user_token": point.token_user,
        }
        for point in results
    ]
