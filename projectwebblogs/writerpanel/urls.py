from django.urls import  path
from .views import deleteData, displayForm, editData, insertData, panel, updateData

#นิยาม กำหนด path ในการเข้าถึงข้อมูลภายในตัว server ว่า user ส่งคำขอมาที่ path อะไร
urlpatterns = [ 
    # หน้าแรก
    path('',panel,name="panel"),
    # แสดงแบบฟอร์มบทความ ให้นักเขียน
    path('displayForm',displayForm,name="displayForm"),
    # บันทึกข้อมูล
    path('insertData',insertData,name="insertData"),
    # ลบข้อมูล ผ่าน id บทความ
    path('deleteData/<int:id>',deleteData,name="deleteData"),
    # แก้ไขข้อมูล ผ่าน id บทความ
    path('editData/<int:id>',editData,name="editData"),
    # อัพเดตข้อมูล ผ่าน id บทความ
    path('updateData/<int:id>',updateData,name="updateData"),

]