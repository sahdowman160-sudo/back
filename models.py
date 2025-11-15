from sqlalchemy import Column, Integer, String , Float ,JSON , Text ,DateTime
from database import Base , engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    code = Column(Integer)
    active=  Column(Integer, default=0)
    token_user = Column(String(200) ,default="0") 


class Proudect(Base):
    __tablename__ = "proudect"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)
    caption =  Column(String(120))
    image = Column(Text)
    category = Column(String(200)) 
    rating = Column(String(200)) 
    reviews = Column(String(200)) 
    originalPrice = Column(String(200)) 
class Addvertise(Base):
    __tablename__ = "addvertise"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)
    caption =  Column(String(120))
    image = Column(Text)
    category = Column(String(200)) 
    rating = Column(String(200)) 
    reviews = Column(String(200)) 
    originalPrice = Column(String(200)) 

class Cart(Base):
    __tablename__ = "Cart"

    id = Column(Integer, primary_key=True, index=True)
    id_product= Column(Integer)
    price = Column(Float)
    quantity =  Column(Integer)
    size = Column(String(120)) 
    token_user = Column(String(200))

class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    token_user = Column(String(200)) 

class Bay(Base):
    __tablename__ = "Bay"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(String(120), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(String(50), nullable=False)
    phone1 = Column(String(50), nullable=False)
    phone2 = Column(String(50), nullable=False)
    stute = Column(String(120), default="تم الطلب")
    time = Column(DateTime)
    way_payment = Column(String(120), nullable=False)
    loction = Column(String(255), nullable=False)
    token_user = Column(String(200)) 
class Notifition(Base):
    __tablename__ = "Notifition"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    message =  Column(String(120))
class Point(Base):
    __tablename__ = "Point"

    id = Column(Integer, primary_key=True, index=True)
    point = Column(Integer , default=0)
    token_user = Column(String(200)) 

Base.metadata.create_all(bind=engine)
