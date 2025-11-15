
from fastapi import Depends, APIRouter
from schemas import  Settings , get_settings

router = APIRouter()



@router.post("/settings")
def read_settings(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user
    }
