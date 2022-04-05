from django.contrib import admin
from .models import Blogs
# Register your models here.

#ส่ง model บทความมาให้ admin จัดการ
admin.site.register(Blogs)