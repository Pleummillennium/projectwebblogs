from django.db import models
# Create your models here.

    # ออกแบบโครงสร้าง ฐานข้อมูล ของหมวดหมู่บทความ
    # unique=True ห้ามตั้งชื่อหมวดหมู่บทความซ้ำกัน
class Category (models.Model):
    name = models.CharField(max_length=255,unique=True)

    # function ในการแปลงข้อมูลจาก object เป็น String
    # self.name เอาชื่อ หมวดหมู่ มาแสดงผล 
    def __str__(self):
        return self.name