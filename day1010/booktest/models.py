from django.db import models

# Create your models here.

class BookInfoManager(models.Manager):
    '''图书模型管理器类'''
    # 1.改变原有查询的结果集
    def all(self):
        # 1.调用父类的 all 方法，获取所有数据
        books = super().all() # QuerySet
        # 2.对 books 中的数据进行过滤
        books = books.filter(isDelete=False)
        # 返回 books
        return books
    
    def create_book(self, btitle, bpub_data):
        '''添加一本图书'''
        # 1.创建一个图书对象
        # 获取 self 所在的模型类
        model_class = self.model
        book = model_class()
        # book = BookInfo()
        book.btitle = btitle
        book.bpub_data = bpub_data
        # 2.添加进数据库
        book.save()
        # 3.返回 book
        return book


class BookInfo(models.Model):
    btitle = models.CharField(max_length= 20)
    bpub_data = models.DateField()
    # 阅读量，default 是在 django 的逻辑层（模型类层），而不是数据库中
    bread = models.IntegerField(default=0)

    # 价格,最大位数为 10,小数为 2
    bprice = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    # 评论量
    bcomment = models.IntegerField(default=0)

    # 删除标记
    isDelete = models.BooleanField(default=False)

    # override 了 objects 
    objects = BookInfoManager()

    # 重写 str 后，打印对象会得到 return 返回的内容
    def __str__(self) -> str:
        return self.btitle

class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=False)
    hcomment = models.CharField(max_length=100)
    isDelete = models.BooleanField(default=False)
    # on_delete=models.CASCADEon_delete=models.CASCADE
    # 删除 BookInfo 里面的书籍时，会自动删除依赖该书籍的英雄信息
    hbook = models.ForeignKey('BookInfo',on_delete=models.CASCADE,)

    # 暂定
    def __str__(self) -> str:
        return self.hname

class NewsType(models.Model):
    # 类型名
    type_name = models.CharField(max_length=20)
    # 关系属性，代表类型下面的信息
    type_news = models.ManyToManyField('NewsInfo')
    # 新闻类

    def __str__(self):
        return self.type_name

class NewsInfo(models.Model):
    # 新闻标题
    title = models.CharField(max_length=128)
    # 发布时间，自动添加
    pub_date = models.DateTimeField(auto_now_add=True)
    # 信息内容
    content = models.TextField()
    # 关系属性, 代表信息所属的类型,注意不能和上面的同时开启
    #news_type = models.ManyToManyField('NewsType')

# 自关联的模型类设计
class Areas(models.Model):
    '''地区模型类'''
    # 地区名称
    atitle = models.CharField(max_length=20)
    # 关系属性，代表当前地区的父级地区
    aParent = models.ForeignKey('self', null=True,blank=True,on_delete=models.CASCADE,)

    def __str__(self):
        return self.atitle

    def parent(self):
        if self.aParent is None:
            return ''
        return self.aParent.atitle

    parent.short_description = '父级地区名称'

class PicTest(models.Model):
    '''上传图片'''
    goods_pic = models.ImageField(upload_to='booktest')


from tinymce.models import HTMLField
class GoodsInfo(models.Model):
    gcontent=HTMLField()