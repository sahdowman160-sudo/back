from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.orm import Session
import aiohttp
import json
import sys
import os
import tempfile

# إعداد المسار للوصول للمجلدات
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from database import get_db
import models

router = APIRouter()

# إعداد مفتاح وموقع imgbb
API_KEY = "8c53fa8c7105711e7390e788f2aed62d"
API_URL = f"https://api.imgbb.com/1/upload?key={API_KEY}"


# 🔹 دالة رفع صورة إلى imgbb
async def upload_to_imgbb(file: UploadFile):
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        async with aiohttp.ClientSession() as session:
            with open(tmp_path, "rb") as f:
                form_data = aiohttp.FormData()
                form_data.add_field("image", f, filename=file.filename)
                async with session.post(API_URL, data=form_data) as resp:
                    result = await resp.json()
                    if result.get("data") and result["data"].get("url"):
                        return result["data"]["url"]
                    else:
                        print("Upload failed:", result)
                        return None
    except Exception as e:
        print("Error uploading to imgbb:", e)
        return None


# 🔹 Endpoint لإضافة المنتج
@router.post("/insert_proudect")
async def insert_product(
    name: str = Form(...),
    caption: str = Form(...),
    price: float = Form(...),
    originalPrice: str = Form(...),
    category: str = Form(...),
    rating: str = Form(...),
    reviews: str = Form(...),
    images: list[UploadFile] = Form(...),  # ✅ مصفوفة صور
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        # 🔁 نرفع كل صورة على imgbb
        for img in images:
            uploaded_url = await upload_to_imgbb(img)
            if uploaded_url:
                image_urls.append(uploaded_url)

        # ✅ حفظ المنتج في قاعدة البيانات
        new_product = models.Proudect(
            name=name,
            caption=caption,
            price=price,
            category=category,
            rating=rating,
            reviews=reviews,
            originalPrice=originalPrice,
            image=json.dumps(image_urls)
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "status": "success",
            "message": "✅ Product created and all images uploaded successfully",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "caption": new_product.caption,
                "price": new_product.price,
                "category":new_product.category,
                "rating":new_product.rating,
                "reviews":new_product.reviews,
                "originalPrice":new_product.originalPrice,
                "images": image_urls
            }
        }

    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
        return {"status": "error", "detail": str(e)}
