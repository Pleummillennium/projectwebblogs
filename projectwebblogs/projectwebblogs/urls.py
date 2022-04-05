"""projectwebblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

#ตั้งค่า ในการเรียกใช้ตำแหน่งที่อยู่ของรูปภาพ ที่อยู่ในเครื่อง server ร่วมกับตัว models ใน blogs
urlpatterns = [
    # path หน้าแอดมิน
    path('admin/', admin.site.urls),
    # path หน้บทความ
    path('',include("blogs.urls")),
    # อยากเรียกใช้งาน app อะไร ก็ให้เรียกใช้ url ที่เราตั้งชื่อไว้
    # path หน้านักเขียน
    path('writer/dashboard/',include("writerpanel.urls")),
    # path หน้าสมัครสมาชิกเป็นนักเขียน
    path('user/',include("loginsystem.urls")),
   
]

#เอาไว้เช็คว่ามีบัคมั้ย
if settings.DEBUG:
    #ดึงเอา MEDIA_URL และ MEDIA_ROOT จากใน settings มาใช้งาน
    # document_root คือ ตำแหน่งที่เก็บไฟล์ภาพใน server
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)