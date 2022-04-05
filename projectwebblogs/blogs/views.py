from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
# ใช้สำหรับการแบ่งหน้า
from django.core.paginator import Paginator , EmptyPage , InvalidPage
#   ทริค function get() ดึงข้อมูลได้ id เดียว filter() ดึง กี่ id ก็ได้ตามที่เราต้องการ ใน database

# function หน้าแรก
# function สำหรับให้ User ส่งคำขอมาที่ Function นี้ และ Function นี้จะส่งข้อมูลตอบกลับไปหา User
def index(request):
    # Category.objects.all นำข้อมูล หมวดหมู่ ทั้งหมดจาก models category มาเอาไว้ในตัวแปร categories
    categories =  Category.objects.all()
    
    # Blogs.objects.all() นำข้อมูล บทความ ทั้งหมดจาก models blogs มาเอาไว้ในตัวแปร blogs
    blogs = Blogs.objects.all()

    # order_by('-pk') ดึงข้อมูล จากใหม่ไปเก่า
    # [:4] นำ 4 บทความล่าสุดมาใช้
    latest = Blogs.objects.all().order_by('-pk')[:4]

    # แบ่งบทความทั้งหมด ให้แสดงแค่ 4 หน้า
    paginator = Paginator(blogs,4)

    # บทความยอดนิยม
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก แต่เราต้องการ มากไปน้อย ก็ให้ '-views' / [:3] = 3 บทความ views เยอะสุด
    popular = Blogs.objects.all().order_by('-views')[:3]

    # บทความแนะนำ เหมือน ยอดนิยมทุกอย่าง แค่ ไม่เติม - ข้างหน้า views
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก  [:3] = 3 บทความ views น้อยสุด
    suggestion = Blogs.objects.all().order_by('views')[:3]

    # ดักจับข้อผิดพลาด ถ้ามีข้อผิดพลาดเกิดขึ้น except จะทำงาน
    try: 
        # ('page','1') กำหนด page ค่าเริ่มต้นเป็น 1
        page = int(request.GET.get('page','1'))
    except:
    # ถ้า page ไม่มีการนิยามค่า ก็ให้เท่ากับ 1
        page = 1

    # ดักจับข้อผิดพลาด ถ้ามีข้อผิดพลาดเกิดขึ้น except จะทำงาน
    try :
        # นำ paginator มาใช้งาน เก็บไว้ใน blogPeroage 
        # page(page) ให้จำนวนบทความอ้างอิงตาม (blogs,4)
        blogPerpage = paginator.page(page)

    # ถ้าเกิด เหตุการณ์ EmptyPage,InvalidPage except จะทำงาน
    # EmptyPage = หน้าว่าง , InvalidPage = หน้าไม่ถูกต้อง
    except (EmptyPage,InvalidPage):
        # เอา page หน้าสุดท้ายจากการแบ่ง มากำหนดลงไปใน blogPeroage
        # คือถ้าหา page ไม่เจอ จะให้มันไปเปิดที่หน้าสุดท้าย
        blogPerpage = paginator.page(paginator.num_pages)

    # {'categories':categories}) ส่งข้อมูล จากตัวแปร categories ไปทำงานจริงใน index.html
    # {''blogs':blogPeroage}) ส่งข้อมูล จากตัวแปร  blogPeroage ไปทำงานจริงใน index.html
    # latest ส่งข้อมูล ไปทำงานจริงใน index.html
    # popular ส่งข้อมูล ไปทำงานจริงใน index.html
    # suggestion ส่งข้อมูล ไปทำงานจริงใน index.html
    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'latest':latest,'popular':popular,'suggestion':suggestion})

# function เนื้อหาบทความ
# function เมื่อเราส่ง id มา จะแสดงหน้าเว็บ blogDetail ออกมา
def blogDetail(request,id):

     # Category.objects.all นำข้อมูล หมวดหมู่ ทั้งหมดจาก models category มาเอาไว้ในตัวแปร categories
    categories =  Category.objects.all()

    # บทความยอดนิยม
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก แต่เราต้องการ มากไปน้อย ก็ให้ '-views' / [:3] = 3 บทความ views เยอะสุด
    popular = Blogs.objects.all().order_by('-views')[:3]

    # บทความแนะนำ เหมือน ยอดนิยมทุกอย่าง แค่ ไม่เติม - ข้างหน้า views
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก  [:3] = 3 บทความ views น้อยสุด
    suggestion = Blogs.objects.all().order_by('views')[:3]

    # ดึงข้อมูล ที่มี id ตาม id ที่ส่งเข้ามา
    # id แรก = ชื่อ column ใน database
    # id ตัวที่สอง = id ที่เราส่งมา
    singleblog = Blogs.objects.get(id=id)

    # นำ singleblog.views มาใช้ และ ถ้า อ่านบทความใด 1 ครั้ง ให้เพิ่ม ยอดวิวนั้น + 1 
    singleblog.views = singleblog.views + 1

    # ถ้าเกิดการเปลื่ยนแปลงแล้วให้บันทึก
    singleblog.save()

    # {'blog':singleblog} = ข้อมูลที่เก็บไว้ใน singleblog ที่มาจาก logs.objects.get(id=id) ถูกเก็บไว้ใน 'blog' แล้ว
    # จะเอาไปเรียกใช้ใน HTML ก็ {{blog.ตามด้วยชื่อ column ใน database ที่เราต้องการแสดงผล}} เช่น อยากได้ชื่อ ตาม id blog ที่เราเลือก {{blog.name}}
    # {'categories':categories}) ส่งข้อมูล จากตัวแปร categories ไปทำงานจริงใน blogDetail.html
    # popular ส่งข้อมูล ไปทำงานจริงใน blogDetail.html
    # suggestion ส่งข้อมูล ไปทำงานจริงใน blogDetail.html
    return render(request,"frontend/blogDetail.html",{'blog':singleblog,'categories':categories,'popular':popular,'suggestion':suggestion})

# function หาหมวดหมู่
def searchCategory(request,cat_id):

    # Category.objects.all นำข้อมูล หมวดหมู่ ทั้งหมดจาก models category มาเอาไว้ในตัวแปร categories
    categories =  Category.objects.all()

    # บทความยอดนิยม
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก แต่เราต้องการ มากไปน้อย ก็ให้ '-views' / [:3] = 3 บทความ views เยอะสุด
    popular = Blogs.objects.all().order_by('-views')[:3]

    # บทความแนะนำ เหมือน ยอดนิยมทุกอย่าง แค่ ไม่เติม - ข้างหน้า views
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก  [:3] = 3 บทความ views น้อยสุด
    suggestion = Blogs.objects.all().order_by('views')[:3]

    # ดึง บทความ เฉพาะ หมวดหมู่ เดียวกัน / category_id = ชื่อ colum cat_id = ชื่อ พารามิเตอร์ที่ส่งไป
    blogs = Blogs.objects.filter(category_id=cat_id)

    # เอาชื่อ หมวดหมู่ ตาม id มา เก็บไว้ใน ตัวแปร categoriesName
    categoriesName = Category.objects.get(id=cat_id)

    #เอาไปแสดงผล โดยการส่งไปที่ ไฟล์ searchCategory.html
    return render(request,"frontend/searchCategory.html",{"blogs":blogs,'popular':popular,'suggestion':suggestion,'categories':categories,'categoriesName':categoriesName})

# function หาผู้เขียน
def searchWriter(request,writer):

    # Category.objects.all นำข้อมูล หมวดหมู่ ทั้งหมดจาก models category มาเอาไว้ในตัวแปร categories
    categories =  Category.objects.all()

     # บทความยอดนิยม
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก แต่เราต้องการ มากไปน้อย ก็ให้ '-views' / [:3] = 3 บทความ views เยอะสุด
    popular = Blogs.objects.all().order_by('-views')[:3]

    # บทความแนะนำ เหมือน ยอดนิยมทุกอย่าง แค่ ไม่เติม - ข้างหน้า views
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก  [:3] = 3 บทความ views น้อยสุด
    suggestion = Blogs.objects.all().order_by('views')[:3]

    # ดึง บทความ เฉพาะ หมวดหมู่ เดียวกัน / writer = ชื่อ colum writer(หลัง) = ชื่อ พารามิเตอร์ที่ส่งไป
    blogs = Blogs.objects.filter(writer=writer)

    return render(request,"frontend/searchWriter.html",{"blogs":blogs,'popular':popular,'suggestion':suggestion,'categories':categories,'writer':writer})

def searchData (request):
    
    # Category.objects.all นำข้อมูล หมวดหมู่ ทั้งหมดจาก models category มาเอาไว้ในตัวแปร categories
    categories =  Category.objects.all()

    # บทความยอดนิยม
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก แต่เราต้องการ มากไปน้อย ก็ให้ '-views' / [:3] = 3 บทความ views เยอะสุด
    popular = Blogs.objects.all().order_by('-views')[:3]

    # บทความแนะนำ เหมือน ยอดนิยมทุกอย่าง แค่ ไม่เติม - ข้างหน้า views
    #เรียงลำดับบทความตาม จำนวน views
    # order_by = เรียงจากน้อยไปมาก  [:3] = 3 บทความ views น้อยสุด
    suggestion = Blogs.objects.all().order_by('views')[:3]

    # Blogs.objects.all() นำข้อมูล บทความ ทั้งหมดจาก models blogs มาเอาไว้ในตัวแปร blogs
    blogs = Blogs.objects.all()

    if request.method == "POST":
        searchdata = request.POST['searchdata']

    # searchnames = Blogs.objects.all(name=searchname)

    return render(request,"frontend/searchData.html",{'searchdata':searchdata,'blogs':blogs,'popular':popular,'suggestion':suggestion,'categories':categories,})