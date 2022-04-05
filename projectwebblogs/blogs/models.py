from distutils.command.upload import upload
from unicodedata import category
from django import views
from django.db import models
from category.models import Category
# Create your models here.

    # ออกแบบโครงสร้าง ฐานข้อมูล ของบทความ
class Blogs(models.Model):
    # max_length=255 จำกัดการพิมพ์ 255 ตัว
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    # กำหนด 1 บทความจำเป็นต้องมี 1 หมวดหมู่ และ ลบหมวดหมู่ทิ้งก่อนไม่ได้ ถ้ายังเชื่อมโยงกัน ต้องลบบทความก่อน
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    writer = models.CharField(max_length=255)
    # default=0 กำหนดยอด view เป็น 0 เพราะ ยังไม่มีคนดู
    views = models.IntegerField(default=0)
    # upload_to="blogs" เอารูปภาพที่ user อัพมาไปเก็บไว้ใน Folder ชื่อ blogImage / blank=True คือใส่รูปก็ได้ไม่ใส่ก็ได้
    image =  models.ImageField(upload_to="blogImage",blank=True)
    # auto_now_add=True บันทึกเวลาที่ สร้าง บทความ
    created =  models.DateTimeField(auto_now_add=True)

    # function ในการแปลงข้อมูลจาก object เป็น String
    # self.name เอาชื่อ บทความ มาแสดงผล 
    def __str__(self):
        return self.name