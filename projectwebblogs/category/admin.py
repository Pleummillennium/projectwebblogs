from django.contrib import admin
from .models import Category
# Register your models here.

#ส่ง model หมวดหมู่มาให้ admin จัดการ
admin.site.register(Category)