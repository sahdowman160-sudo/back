from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# إعدادات الاتصال بقاعدة البيانات
db_user = "root"
db_pass = "7bfawuufiuxmbhhd"         # حط باسورد MySQL هنا لو فيه
db_host = "vems-vems-wdjhw0"
db_name = "mysql"

# محرك قاعدة البيانات
engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}?charset=utf8mb4",
    echo=True  # يخلي SQL يظهر في اللوج
)

# Base class للـ Models
Base = declarative_base()

# Session لإدارة المعاملات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# dependency عشان نستخدم DB في أي endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
