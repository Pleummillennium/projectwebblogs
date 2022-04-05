from django.urls import  path
from .views import index,blogDetail, searchCategory, searchWriter,searchData

#นิยาม กำหนด path ในการเข้าถึงข้อมูลภายในตัว server ว่า user ส่งคำขอมาที่ path อะไร
urlpatterns=[ 
    # path เปล่าๆ '' คือ หน้าแรก
    path('',index,name="blogindex"),
    # แสดงเนื้อหา บทความ โดยการอ้างอิง id blog จาก server
    # blogDetail = function ที่เรียกใช้ จาก views.py
    # name="blogDetail" คือ การตั้งชื่อ path
    path('blog/<int:id>',blogDetail,name="blogDetail"),
    # แสดงเนื้อหา หมวดหมู่ โดยการอ้างอิง category_id จาก server
    # int = กำหนดเป็นจำนวนเต็มตาม modal :cat_id = ชื่อพารามิเตอร์ที่เราตั้ง
    # name="searchCategory" คือ การตั้งชื่อ path ที่เราจะเรียกใช้ใน html เช่น {% url 'searchCategory' blog.category_id%}
    path('blog/category/<int:cat_id>',searchCategory,name="searchCategory"),
    # path ในการ ค้นหา บทความตามชื่อนักเขียน
    # str = กำหนดเป็นตัวอักษรตาม modal :writer = ชื่อพารามิเตอร์ที่เราตั้ง
    path('blog/writer/<str:writer>',searchWriter,name="searchWriter"),
    path('searchdata',searchData,name="searchData"),

]