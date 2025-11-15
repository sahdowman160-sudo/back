from fastapi import FastAPI
from routers.user import send_email,points,change_password,addverise,fitroom,cancel_order, get_buy,login,show_like,delet_cart,delete_like, check_add ,users , proudect ,search,select_proudect, cart , bay,insert_cart , get_like , extrct_token , get_notifiction , like
from routers.super_admin import extrxt_super,add_admin,insert_proudect,notfiction
from routers.admin import delete,count,cart_admin,money,totl_user,change_stute,get_bayA,admin,insert_proudect,notfiction
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين الراوتر داخل التطبيق
app.include_router(login.router)
app.include_router(extrxt_super.router)
app.include_router(delete.router)
app.include_router(points.router)
app.include_router(send_email.router)
app.include_router(change_password.router)
app.include_router(addverise.router)
app.include_router(count.router)
app.include_router(cart_admin.router)
app.include_router(money.router)
app.include_router(totl_user.router)
app.include_router(fitroom.router)
app.include_router(change_stute.router)
app.include_router(cancel_order.router)
app.include_router(add_admin.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(proudect.router)
app.include_router(insert_proudect.router)
app.include_router(insert_cart.router)
app.include_router(cart.router)
app.include_router(notfiction.router)
app.include_router(extrct_token.router)
app.include_router(get_notifiction.router)
app.include_router(bay.router)
app.include_router(like.router)
app.include_router(get_like.router)
app.include_router(search.router)
app.include_router(select_proudect.router)
app.include_router(check_add.router)
app.include_router(delet_cart.router)
app.include_router(delete_like.router)
app.include_router(show_like.router)
app.include_router(get_buy.router)
app.include_router(get_bayA.router)