from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import time
import requests
import re
import shutil
from playwright.sync_api import sync_playwright, Page, expect, TimeoutError
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.post("/try_on")
def try_on_api(
    clothes: UploadFile = File(...),
    model: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    RESULTS_DIR = "results"
    TEMP_DIR = "temp"
    HEADLESS_MODE = True  # لتجعل المتصفح ظاهر أثناء التشغيل (لو حبيت تخليه خفي: True)
    TEMP_MAIL_API = "https://api.mail.tm"
    MAGIC_LINK_TIMEOUT = 120  # مهلة انتظار الإيميل المؤقت

    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 🖼️ حفظ صور الملابس والموديل مؤقتًا
    clothes_path = os.path.join(TEMP_DIR, f"clothes_{int(time.time())}.jpg")
    model_path = os.path.join(TEMP_DIR, f"model_{int(time.time())}.jpg")

    with open(clothes_path, "wb") as f:
        f.write(clothes.file.read())
    with open(model_path, "wb") as f:
        f.write(model.file.read())

    # 📧 إنشاء إيميل مؤقت والحصول على رابط الدخول (magic link)
    def get_temp_email_and_magic_link(page: Page) -> str:
        session = requests.Session()
        try:
            domain = session.get(f"{TEMP_MAIL_API}/domains").json()['hydra:member'][0]['domain']
            password = os.urandom(12).hex()
            email = f"{os.urandom(8).hex()}@{domain}"
            payload = {"address": email, "password": password}
            res = session.post(f"{TEMP_MAIL_API}/accounts", json=payload)
            if res.status_code != 201:
                raise Exception(f"فشل إنشاء الإيميل: {res.text}")
            page.locator("input[placeholder='Enter your email']").fill(email)
            page.get_by_role("button", name="Continue with Email").click()
            token = session.post(f"{TEMP_MAIL_API}/token", json=payload).json()["token"]
            headers = {"Authorization": f"Bearer {token}"}
            start = time.time()
            while time.time() - start < MAGIC_LINK_TIMEOUT:
                time.sleep(5)
                msgs = session.get(f"{TEMP_MAIL_API}/messages", headers=headers).json().get('hydra:member', [])
                for msg in msgs:
                    data = session.get(f"{TEMP_MAIL_API}/messages/{msg['id']}", headers=headers).json()
                    content = (data.get("text", "") + "".join(data.get("html", [])))
                    match = re.search(r'(https://quickchange-prod\.firebaseapp\.com/__/auth/action\?[^>\s]+)', content)
                    if match:
                        return match.group(1).replace("&amp;", "&").strip().replace("'", "")
            raise TimeoutError("⏰ لم يصل رابط الدخول.")
        except Exception:
            return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS_MODE, slow_mo=50)
            page = browser.new_page()
            page.goto("https://fitroom.app/editor", timeout=90000)

            # 🚫 حجب الإعلانات قبل تحميل الصفحة
            page.route(
                "**/*",
                lambda route: route.abort()
                if any(x in route.request.url for x in ["ads", "googlesyndication", "doubleclick", "googletagservices"])
                else route.continue_()
            )

            # 🧹 حذف أي إعلانات ظهرت فعلاً بعد التحميل
            try:
                time.sleep(3)
                page.evaluate("""
                () => {
                    document.querySelectorAll("iframe[src*='ads'], iframe[src*='googlesyndication'], iframe[src*='doubleclick']")
                        .forEach(el => el.remove());
                    document.querySelectorAll("div[id*='ad'], div[class*='ad'], span[class*='ad'], section[id*='ad']")
                        .forEach(el => el.remove());
                }
                """)
                print("🧹 تم حذف الإعلانات من الصفحة بنجاح.")
            except Exception as e:
                print(f"⚠️ فشل حذف الإعلانات أو لم توجد: {e}")

            # 🔐 تسجيل الدخول
            print("🔐 تسجيل الدخول...")
            page.get_by_role("button", name="Sign in", exact=True).click()
            link = get_temp_email_and_magic_link(page)
            if not link:
                raise Exception("لم يتم استلام رابط الدخول")
            page.goto(link, timeout=90000)

            # 🚀 الانتقال إلى صفحة المحرر
            try:
                page.wait_for_url("**/create", timeout=20000)
                page.goto("https://fitroom.app/editor", timeout=60000)
            except TimeoutError:
                page.goto("https://fitroom.app/editor", timeout=60000)
            page.wait_for_url("**/editor", timeout=60000)
            print("✅ داخل المحرر.")

            # ✅ إغلاق نافذة FitRoom PRO (الكود الجديد من الجزء الثاني)
            print("🔎 البحث عن نافذة FitRoom PRO...")
            try:
                path_selector = "div.cursor-pointer svg path[d^='M3.33398']"
                time.sleep(5)  # انتظار بسيط لتحميل الواجهة
                page.wait_for_selector(path_selector, timeout=15000)
                popup = page.locator(path_selector).first
                if popup.is_visible():
                    popup.evaluate("node => node.closest('div.cursor-pointer').click()")
                    print("✅ تم إغلاق نافذة FitRoom PRO.")
                else:
                    print("ℹ️ لم تظهر نافذة FitRoom PRO.")
            except TimeoutError:
                print("ℹ️ لم تظهر نافذة FitRoom PRO خلال المهلة المحددة.")
            except Exception as e:
                print(f"⚠️ حدث خطأ أثناء محاولة إغلاق نافذة FitRoom PRO: {e}")

            # 👕 رفع صورة الملابس
            print(f"👕 رفع الملابس: {clothes_path}")
            clothes_input = page.locator("input[type='file']").first
            page.evaluate("""
            () => {
                const input = document.querySelectorAll("input[type='file']")[0];
                input.removeAttribute('hidden');
                input.style.display = 'block';
                input.style.visibility = 'visible';
                input.style.opacity = '1';
            }
            """)
            clothes_input.set_input_files(clothes_path)
            expect(page.locator("img[alt='outfit']")).to_be_visible(timeout=90000)
            print("✅ ظهرت معاينة الملابس.")

            # 🧍‍♀️ رفع الموديل
            print(f"🧍‍♀️ رفع الموديل: {model_path}")
            model_input = page.locator("input[type='file']").nth(3)
            page.evaluate("""
            () => {
                const inputs = document.querySelectorAll("input[type='file']");
                const m = inputs[3];
                m.removeAttribute('hidden');
                m.style.display = 'block';
                m.style.visibility = 'visible';
                m.style.opacity = '1';
            }
            """)
            model_input.set_input_files(model_path)
            print("📤 رفع الموديل جاري...")

            try:
                page.wait_for_selector("div.absolute.z-20.inset-0.bg-neutral-ink-600", timeout=120000)
                print("✅ بدأ رفع الموديل — سيتم الآن الضغط على Generate.")
            except TimeoutError:
                print("⚠️ لم يظهر العنصر خلال دقيقتين.")

            # ⚙️ الضغط على Generate
            print("⚙️ الضغط على Generate...")
            gen_btn = page.get_by_role("button", name="Generate")
            expect(gen_btn).to_be_enabled(timeout=20000)
            gen_btn.click()
            print("🚀 بدأ التوليد...")

            # ⏳ انتظار الصورة الناتجة
            print("⏳ انتظار النتيجة حتى تظهر...")
            result_url = None
            for _ in range(180):
                imgs = page.locator("img[alt='result']")
                for i in range(imgs.count()):
                    src = imgs.nth(i).get_attribute("src")
                    if src and src.startswith("https://userimage.fitroom.app"):
                        result_url = src
                        break
                if result_url:
                    break
                time.sleep(1)
            if not result_url:
                raise Exception("❌ لم تظهر النتيجة خلال 3 دقائق.")
            print(f"✅ النتيجة: {result_url}")

            # 💾 حفظ الصورة الناتجة
         
            browser.close()
            return JSONResponse({"status": "success", "result_url": result_url})

    except Exception as e:
        print("❌ خطأ:", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 🧹 تنظيف مجلد temp بعد انتهاء العملية
        try:
            if os.path.exists(TEMP_DIR):
                for filename in os.listdir(TEMP_DIR):
                    file_path = os.path.join(TEMP_DIR, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                print("🧹 تم حذف جميع الصور المؤقتة بنجاح.")
        except Exception as cleanup_error:
            print(f"⚠️ فشل حذف الملفات المؤقتة: {cleanup_error}")
