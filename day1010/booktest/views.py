from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from booktest.models import BookInfo, Areas, GoodsInfo
from datetime import date
from django.db.models import F,Q
from django.db.models import Sum,Count,Max,Min,Avg
from datetime import datetime,timedelta

def index(request):
    # return HttpResponse('hello python')
    return render(request, 'index.html', {'content':'hello world'})

def index2(request):
    # 练习 Q 对象
    print(BookInfo.objects.filter(Q(id__gt=2) & Q(bread__gt=19)))
    return HttpResponse('hello python')

def show_books(request):
    books = BookInfo.objects.all()
    return render(request, 'showbooks.html', {'books': books})

def detail(request, bid):
    book = BookInfo.objects.get(id = bid)
    heros = book.heroinfo_set.all()
    return render(request, 'detail.html', {'book':book, 'heros':heros})
    
def create(request):
    '''新增一本图书'''
    # 1.创建 BookInfo 对象
    b = BookInfo()
    b.btitle = 'C 语言开发宝典'
    b.bpub_data = date(2019,10,1)
    # 2.保存进数据库
    b.save()
    # 3.返回应答,让浏览器再访问/books,重定向
    return HttpResponseRedirect('/books')

def delete(request, bid):
    '''删除点击的图书'''
    book = BookInfo.objects.get(id = bid)
    book.delete()
    return HttpResponseRedirect('/books')

def use_aggregate(request):
    print(BookInfo.objects.all().aggregate(Count('id')))
    print(BookInfo.objects.aggregate(Sum('bread')))

    # count() 的特殊待遇
    print(BookInfo.objects.all().count())
    print(BookInfo.objects.count())

    print(BookInfo.objects.filter(id__gt=3).count())

    return HttpResponse('ok')


def areas(request):
    '''获取广州市的上级地区和下级地区'''
    # 1.获取广州市的信息
    area = Areas.objects.get(atitle='广州市')
    # 2.查询广州市的上级地区
    parent = area.aParent
    # 3.查询广州市的下级地址
    children = area.areas_set.all()
    # 使用模板
    return render(request, 'area.html', {'area':area,'parent':parent, 'children':children})

def login(request):
    # # 判断用户是否登录
    # if request.session.has_key('islogin'):
    # # 用户已登录, 跳转到首页
    #     return HttpResponseRedirect('/index')

    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''

    return render(request, 'login.html', {'username':username})

def login_check(request):
    '''登录校验视图'''
    # 获取用户输入验证码
    vcode1 = request.POST.get('vcode')
    # 获取 session 中保存的验证码
    vcode2 = request.session.get('verifycode')
    # 进行验证码校验
    if vcode1 != vcode2:
        # 验证码错误
        return HttpResponseRedirect('/login')

    # request.POST 保存的是 post 方式提交的参数 QueryDict
    # request.GET 保存是 get 方式提交的参数 类型也是 QueryDict
    username=request.POST.get('username')
    password=request.POST.get('password')
    remember = request.POST.get('remember') # add

    # just an example
    if username == 'akashi' and password == '123':
        resp =  HttpResponseRedirect('/index')
        request.session['islogin'] = True
        if remember == 'on':
            resp.set_cookie('username', username, max_age=7*24*3600)
        return resp

    else:
        return HttpResponseRedirect('/login')

def test_ajax(request):
    '''显示 ajax 页面'''
    return render(request, 'test_ajax.html')

def ajax_handle(request):
    '''ajax 请求处理'''
    # 返回的 json 数据 {'res':1}
    return JsonResponse({'res':1})

def login_ajax(request):
    return render(request, 'login_ajax.html')

def login_ajax_check(request):
    '''ajax 登录校验'''
    # 1.获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 2.进行校验,返回 json 数据
    if username == 'admin' and password == '123':
        # 用户名密码正确
        return JsonResponse({'res':1})
        # return redirect('/index') ajax 请求在后台，不要返回页面或者重定向，这样是不行的，一定要返回 Json！
    else:
        # 用户名或密码错误
        return JsonResponse({'res':0})

def set_cookie(request):
    '''设置 cookie 信息'''
    response = HttpResponse('设置 cookie')
    # 设置一个 cookie 信息,名字为 num, 值为 2
    response.set_cookie('num', 2)
    #下面是设置 cookie 在两周之后过期
    # response.set_cookie('num', 2, max_age=14*24*3600)
    # response.set_cookie('num', 1,expires=datetime.now()+timedelta(days=14))
    # 返回 response
    return response

def get_cookie(request):
    '''获取 cookie 的信息'''
    # 取出 cookie num 的值
    num = request.COOKIES['num']
    print(num)
    return HttpResponse(num)

def set_session(request):
    '''设置 session'''
    request.session['username'] = 'yomiya'
    request.session['age'] = 17
    # request.session.set_expiry(5)
    return HttpResponse('设置 session')

def get_session(request):
    '''获取 session'''
    username = request.session['username']
    age = request.session['age']
    return HttpResponse(username+':'+str(age))

# def clear_session(request):
#     '''清除 session 信息'''
#     # request.session.clear()
#     # request.session.flush()
#     return HttpResponse('清除成功')


def test_var(request):
    '''模板变量'''
    my_dict = {'title':'字典键值'}
    my_list = [1,2,3]
    book = BookInfo.objects.get(id=1)
    # 定义模板上下文
    context = {'my_dict':my_dict, 'my_list':my_list, 'book':book}
    return render(request, 'test_var.html', context)

def test_filters(request):
    books = BookInfo.objects.all()
    return render(request, 'test_filters.html', {'books':books})

def test_template_inhert(request):
    # return render(request, "base.html")
    return render(request, "child.html")

def html_escape(request):
    '''html 转义'''
    return render(request, 'html_escape.html',{'content':'<h1>hello</h1>'})


def change_pwd(request):
    return render(request, 'change_pwd.html')

def change_pwd_action(request):
    '''模拟修改密码处理'''
    # 1.获取新密码
    pwd = request.POST.get('pwd')
    # 2.返回一个应答
    return HttpResponse('修改密码为:%s'%pwd)



# /verify_code
from PIL import Image, ImageDraw, ImageFont
# from django.utils.six import BytesIO #django 3 以后丢弃了
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高 RGB
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的 point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取 4 个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 构造字体对象，ubuntu 的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0,255))
    # 绘制 4 个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入 session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为 png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME 类型为图片 png
    return HttpResponse(buf.getvalue(), 'image/png')

def url_reverse(request):
    return render(request, 'url_reverse.html')

def show_args(request, a, b):
    return HttpResponse(str(a) + ':' + str(b))

def show_kwargs(request, c, d):
    return HttpResponse(str(c) + ":" + str(d))


from django.urls import reverse
# /test_redirect
def test_redirect(request):
    # 重定向到/index
    # return redirect('/index')
    # url = reverse('booktest:index')
    # 重定向到/show_args/1/2
    url = reverse('booktest:show_args', args=(1,2))
    # 重定向到/show_kwargs/3/4
    # url = reverse('booktest:show_kwargs', kwargs = {'c': 3, 'd': 4})
    return HttpResponseRedirect(url)

def static_test(request):
    return render(request, "static_test.html")

from booktest.models import PicTest
def pic_show(request):
    pic=PicTest.objects.get(id=1)
    context={'pic':pic}
    return render(request,'pic_show.html',context)

# /show_upload
def show_upload(request):
    '''显示上传图片页面'''
    return render(request, 'upload_pic.html')

from day1010 import settings
def upload_handle(request):
    '''上传图片处理'''
    # 1.获取上传文件的处理对象
    pic = request.FILES['pic']

    # 2.创建一个文件
    save_path = '%s/booktest/%s'%(settings.MEDIA_ROOT,pic.name)
    with open(save_path, 'wb') as f:
        # 3.获取上传文件的内容并写到创建的文件中
        for content in pic.chunks():
            f.write(content)

    # 4.在数据库中保存上传记录
    PicTest.objects.create(goods_pic='booktest/%s'%pic.name)

    # 5.返回
    return HttpResponse('ok')

from django.core.paginator import Paginator
def show_area(request, pindex=1):
    areas = Areas.objects.filter(aParent__isnull=True)

    # 2. 分页,每页显示 10 条
    paginator = Paginator(areas, 10)

    # 3. 获取第 pindex 页的内容
    pindex = int(pindex)
    # page 是 Page 类的实例对象
    page = paginator.page(pindex)

    return render(request, 'show_area.html',{'page': page})



def areas(request):
    '''省市县选中案例'''
    return render(request, 'areas.html')

def prov(request):
    '''获取所有省级地区的信息'''
    # 1.获取所有省级地区的信息
    areas = Areas.objects.filter(aParent__isnull=True)
    # 2.变量 areas 并拼接出 json 数据：atitle id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 3.返回数据
    return JsonResponse({'data':areas_list})

def city(request, pid=0):
    '''获取 pid 的下级地区的信息'''
    # 1.获取 pid 对应地区的下级地区
    # area = AreaInfo.objects.get(id=pid)
    # areas = area.areainfo_set.all()
    areas = Areas.objects.filter(aParent__id=pid)
    # 2.变量 areas 并拼接出 json 数据：atitle id
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.atitle))
    # 3.返回数据,返回给前端，对方得到的是数组
    return JsonResponse({'data': areas_list})

def show(request):
    goods=GoodsInfo.objects.get(pk=1)
    context={'g':goods}
    return render(request,'show.html',context)


# 用户看的富文本编辑器
def editor(request):
    return render(request, 'editor.html')