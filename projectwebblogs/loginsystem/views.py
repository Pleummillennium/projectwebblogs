from urllib import request
from django.shortcuts import redirect, render
# เครื่องมือในการส่งข้อความตอบกลับไปหาผู้ใช้
from django.contrib import messages
# เครื่องมือในการสร้างบัญชีผู้ใช้ auth = ตัวดำเนินการ login/logout
from django.contrib.auth.models import User,auth
# เอา login_register.html มาแสดงผล
def index(request):
    return render(request,"backend/login_register.html")


def register(request):
    # สร้างเงี่อนไขดักไว้ ค่าที่ ส่งมา เป็น POST จริงป่าว
    if request.method == "POST":
        # รับค่าจาก name="" ตามที่ user เขียนมาจาก html มาเก็บในตัวแปร
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        # ถ้า ตัวแปร เป็นค่าว่างจะ ...
        if username == "" or email == "" or password == "" or repassword == "":
            messages.info(request,"กรุณาป้อนข้อมูลให้ครบ")
            return redirect("member")
        else :
            if password == repassword :
                # ถ้า username ซ้ำกัน จะ....
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username นี้มีผู้ใช้แล้ว")
                    return redirect("member")
                # ถ้า email ซ้ำกัน จะ....  
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email นี้เคยลงทะเบียนแล้ว")
                    return redirect("member")
                    
                else:
                    # นิยามการ สร้างบัญชีผู้ใช้
                    user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,)
                    user.save()
                    messages.info(request,"สร้างบัญชีสำเร็จ")
                    return redirect("member")

            else :
                messages.info(request,"ไม่สามารถลงทะเบียนได้รหัสผ่านไม่ตรงกัน")
                return redirect("member")

def login(request):
    # รับค่าจาก name="" ตามที่ user เขียนมาจาก html มาเก็บในตัวแปร
    username = request.POST["username"]
    password = request.POST["password"]
    #เช็คการ login/logout และเก็บข้อมูลของผู้ใช้ที่มีการ login/logout / authenticate = ตรวจสอบว่าเจอ username,password เหมือนกับ ใน database มั้ย
    user = auth.authenticate(username=username,password= password)
    # ถ้าเจอข้อมูลใน database แล้วจะให้ทำ.....
    if user is not None:
        # ให้ login เข้าใช้งานระบบเลย / ส่ง ข้อมูล user ไปด้วย
        auth.login(request,user)
        return redirect("panel")

    # ถ้ารหัสไม่ตรงกับใน database จะ..
    else:
        messages.info(request,"ไม่พบข้อมูลบัญชีผู้ใช้")
        return redirect("member")

def logout(request):
    auth.logout(request)
    return redirect ('member')