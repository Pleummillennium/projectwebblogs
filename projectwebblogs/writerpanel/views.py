from django.shortcuts import redirect, render
# สอบถามข้อมูลบทความ
from blogs.models import Blogs
# ฟังก์ชั่นในการหาผลรวม
from django.db.models import Sum
# อยากดึงชื่อผู้เขียน ต้องล็อคอินก่อน
from django.contrib.auth.decorators import login_required
# เอาช้อมูลของคนที่ login เก็บไว้ แล้วก็เอาไปใช้อะไรก็แล้วแต่
from django.contrib.auth.models import auth
# นำข้อมูลหมวดหมู่มา
from category.models import Category
# ฟังก์ชันสำหรับการเอาไฟล์รูปภาพที่ user ส่งมา เก็บไว้ในโฟลเดอร์ที่เราเลือก
from django.core.files.storage import FileSystemStorage
# เครื่องมือในการส่งข้อความตอบกลับไปหาผู้ใช้
from django.contrib import messages

# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# แสดงข้อมูลบทความของผู้เขียน
def panel(request):
    # ดึงชื่อนักเขียนจาก auth ที่เก็บข้อมูลของผู้เขียนจากการ login มา
    writer = auth.get_user(request)
    # ถ้าชื่อนักเขียน ในตัวแปร writer ตรงกับ ชื่อนักเขียนใน colum ใน database ก็ให้เอาไปเก็บไว้ใน ตัวแปร blogs ซะ  writer=writer ตัวแรก ชื่อ colum ใน database ตัวสอง ขื่อตัวแปรด้านบน
    blogs = Blogs.objects.filter(writer=writer)
    # นับจำนวนบทความทั้งหมดของผู้เขียนแต่ละท่าน
    blogCount = blogs.count()
    # aggregate(Sum(ระบุชื่อ colum ที่จะหาผลรวม)) = หาผลรวม 
    totalViews =  Blogs.objects.filter(writer=writer).aggregate(Sum("views"))

    allblogs = Blogs.objects.all()

    #ส่งไปแสดงผลที่ไฟล์ index.html
    return render(request,"backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"totalViews":totalViews,'allblogs':allblogs})

# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# แสดงแบบฟอร์มให้ผู้เขียน
def displayForm(request):

    # ดึงชื่อนักเขียนจาก auth ที่เก็บข้อมูลของผู้เขียนจากการ login มา
    writer = auth.get_user(request)
    # ถ้าชื่อนักเขียน ในตัวแปร writer ตรงกับ ชื่อนักเขียนใน colum ใน database ก็ให้เอาไปเก็บไว้ใน ตัวแปร blogs ซะ  writer=writer ตัวแรก ชื่อ colum ใน database ตัวสอง ขื่อตัวแปรด้านบน
    blogs = Blogs.objects.filter(writer=writer)
    # นับจำนวนบทความทั้งหมดของผู้เขียนแต่ละท่าน
    blogCount = blogs.count()
    # aggregate(Sum(ระบุชื่อ colum ที่จะหาผลรวม)) = หาผลรวม 
    totalViews =  Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    # ดึงข้อมูลหมวดหมู่ทั้งหมดมาเก็บในตัวแปร 
    categories = Category.objects.all()

    return render(request,"backend/blogForm.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"totalViews":totalViews,"categories":categories})

# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# บันทึกข้อมูลบทความที่เขียน
def insertData(request):
    # ถ้ามีข้อผิดพลาดเกิดขึ้นให้ไปหา panel เลย
    try :
        # request ที่ส่งมาเป็นแบบ POST และเป็น File ที่ชื่อ image มั้ย
        if request.method == "POST" and request.FILES["image"] :
            #รับค่าจาก <form> ใน blogForm.html ที่ชื่อ name"ชื่อที่ตั้ง" ใน <input>
            datafile = request.FILES["image"]
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            # อันนี้เอามาจากคนที่เข้าระบบล็อคอิน
            writer = auth.get_user(request)
            # เช็ค ไฟล์ที่ upload มาเป็นรูปภาพมั้ย
            if str(datafile.content_type).startswith("image"):
                # ถ้าเป็นก็ให้อัพโหลดเก็บไว้ในโฟลเดอร์ blogImage
                fs = FileSystemStorage()
                img_url = "blogImage/"+datafile.name
                filename = fs.save(img_url,datafile)
                # บันทึกข้อมูลบทความ
                # นำมาเก็บไว้ใน field database (colum=ตัวแปร) ใน blogs
                blog = Blogs(
                name = name,
                category_id = category,
                description = description,
                content = content, 
                writer = writer,
                image = img_url,
                )
                # บันทึกข้อมูล
                blog.save()
                # ส่งข้อความไปหน้า displayForm
                messages.info(request,"บันทึกข้อมูลเรียบร้อย")
                return redirect("displayForm")
            else:
                # ส่งข้อความไปหน้า displayForm
                messages.info(request,"ไฟล์ที่อัพโหลดไม่รองรับ กรุณาอัพโหลดไฟล์รูปภาพอีกครั้ง")
                return redirect("displayForm")
    except :
        return redirect("displayForm")

# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# ลบข้อมูลบทความที่เขียน
def deleteData(request,id):
    # ถ้ามีข้อผิดพลาดเกิดขึ้นให้ไปหา panel เลย
    try :
        # ดึงบทความตาม id ใน database
        blog = Blogs.objects.get(id=id)
        # ดึงข้อมูล database ทั้งหมดมาเก็บไว้ใน fs
        fs = FileSystemStorage()
        # นำมูลใน database มาลบ โดยเราจะลบแค่ รูป ก็ใส่ str(blog.image) /เราลบข้อมูลบทความใน blogแล้ว แต่มันไม่ลบรูปให้ด้วยเพราะอยู่คนละ path ข้อมูลปกติจะอยู่ใน blog แต่รูป มันอยู่ใน media ไง จริงๆไม่ก็ไรไม่ส่งผลไรมากหรอกแต่ที่ลบเพราะมันจะได้ไม่รกเครื่อง/ ตอนแรกมันเป็น field ก็เปลื่ยนให้มันเป็นstring ก่อน ก็ใส่ str
        fs.delete(str(blog.image))
        # ลบข้อมูลบทความใน database
        blog.delete()
        return redirect('panel')
    except :
        return redirect("panel")

# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# แก้ไขข้อมูลบทความที่เขียน
def editData(request,id):
    # ดึงบทความตาม id ใน database
    blogEdit = Blogs.objects.get(id=id)

    # ข้อมูลพื้นฐานในการแสดงผล
    # ดึงชื่อนักเขียนจาก auth ที่เก็บข้อมูลของผู้เขียนจากการ login มา
    writer = auth.get_user(request)
    # ถ้าชื่อนักเขียน ในตัวแปร writer ตรงกับ ชื่อนักเขียนใน colum ใน database ก็ให้เอาไปเก็บไว้ใน ตัวแปร blogs ซะ  writer=writer ตัวแรก ชื่อ colum ใน database ตัวสอง ขื่อตัวแปรด้านบน
    blogs = Blogs.objects.filter(writer=writer)
    # นับจำนวนบทความทั้งหมดของผู้เขียนแต่ละท่าน
    blogCount = blogs.count()
    # aggregate(Sum(ระบุชื่อ colum ที่จะหาผลรวม)) = หาผลรวม 
    totalViews =  Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    # ดึงข้อมูลหมวดหมู่ทั้งหมดมาเก็บในตัวแปร 
    categories = Category.objects.all()
    return render(request,"backend/editForm.html",{"blogEdit":blogEdit,"writer":writer,"blogCount":blogCount,"totalViews":totalViews,"categories":categories})
        
# ถ้ายังไม่ login จะบังคับไปหน้า member 
@login_required(login_url="member")
# อัพเดตข้อมูลบทความที่เขียน 
def updateData(request,id):
    # ถ้ามีข้อผิดพลาดเกิดขึ้นให้ไปหา panel เลย
    try :
             # request ที่ส่งมาเป็นแบบ POST 
        if request.method == "POST" :
            # จะอัพเดตต้องดึงข้อมูลเดิมมาก่อนแล้วค่อนเอาข้อมูลใหม่ไปแปะทับ
            # ดึงข้อมูลบทความที่การต้องแก้ไข้มาใช้งาน
            blog = Blogs.objects.get(id=id)
            # รับค่าจาก <form> ใน blogForm.html ที่ชื่อ name"ชื่อที่ตั้ง" ใน <input>
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            # อัพเดตข้อมูล หรือแทนที่ข้อมูล blog.ชื่อfield = ตัวแปร
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            # เซฟทับข้อมูลเก่าด้วยข้อมูลใหม่
            blog.save()

            # อัพเดตภาพปก
            # ส่ง file ใน image มามั้ย
            if request.FILES["image"] :
                #รับค่าจาก <form> ใน blogForm.html ที่ชื่อ name"ชื่อที่ตั้ง" ใน <input>
                datafile = request.FILES["image"]    
                # ถ้าส่ง file มาแล้ว ใช่ file ที่ upload เป็นรูปภาพมั้ย
                if str(datafile.content_type).startswith("image"):
                    # ลบภาพเดิมบทความออกไปก่อน
                    fs = FileSystemStorage()
                    fs.delete(str(blog.image))
                    # แทนที่ด้วยภาพใหม่
                    img_url = "blogImage/"+datafile.name
                    filename = fs.save(img_url,datafile)
                    # อัพเดตภาพปก หรือแทนที่ภาพปก blog.ชื่อfield = ตัวแปร
                    blog.image = img_url
                    # เซฟทับข้อมูลเก่าด้วยข้อมูลใหม่
                    blog.save()
                return redirect("panel")
    
    except :
        return redirect("panel")