from django.urls import  path
from .views import index, login, logout,register

#นิยาม กำหนด path ในการเข้าถึงข้อมูลภายในตัว server ว่า user ส่งคำขอมาที่ path อะไร
urlpatterns = [ 
    # หน้าแรกในส่วนการสมัครสมาชิกการเป็นนักเขียน
    path('member',index,name="member"),
    # ลงทะเบียนสมัครสมาชิก
    path('register/add',register,name="addUser"),
    # เข้าสู่ระบบ
    path('login',login,name="login"),
    path('logout',logout,name="logout")
]