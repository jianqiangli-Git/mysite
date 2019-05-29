from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
# 文章分类数据表(一篇文章只有一个类别)
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# 文章标签数据表(一篇文章可以有多个标签)
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name

class User(models.Model):
    gender = (('F','女'),('M','男'))
    user_name = models.CharField(max_length=10)
    sex = models.CharField(max_length=5,choices=gender)
    leaving_num = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user_name

    def incre_leaving_num(self):
        self.leaving_num += 1;
        # 这里的 self 是 Article 类的当前实例
        self.save(update_fields=['leaving_num'])

# 一个likes看作一个点赞对象
class Likes(models.Model):
    choice = (("article","赞文章"),("person","赞作者"))
    likes_type = models.CharField(max_length=10,choices=choice,default="article") # 我看看是给文章点赞还是给我点赞
    host_name = models.CharField(max_length=30,verbose_name='主机名')
    port = models.CharField(max_length=4,verbose_name='端口')
    ip_address = models.GenericIPAddressField(blank=True, null=True,verbose_name='ip地址')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='点赞的时间')

    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = '文章点赞'
        verbose_name_plural = '文章点赞'


# class ArticleFace(models.Model):
#     img = models.ImageField(upload_to='upload',blank=True,null=True) # 存储路径是相对于MEIDA_ROOT而来的


class Article(models.Model):
    # time ："hh: mm:ss" 格式表示的时间值，格式显示TIME值，但允许使用字符串或数字为TIME列分配值。
    # date ："yyyy - mm - dd" 格式表示的日期值 ，以’HH: MM:SS’格式显示TIME值，但允许使用字符串或数字为TIME列分配值
    # datetime："yyyy - mm - dd hh:mm:ss" 格式，日期和时间的组合。格式显示DATETIME值，但允许使用字符串或数字为DATETIME列分配值。
    choice = (('d', 'draft'), ('p', 'published'))
    # face = models.ForeignKey(ArticleFace,blank=True,null=True,on_delete=models.DO_NOTHING)
    face = models.ImageField(upload_to='upload',blank=True,null=True)   # 文章封面，upload_to指定图片上传的路径，如果不存在则自动创建
    article_name = models.CharField(max_length=50)
    # content = models.TextField()
    content = RichTextUploadingField()
    author = models.ManyToManyField(User)
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE) #删除类别，文章也级联删除
    tag = models.ManyToManyField(Tag,blank=True,null=True) #文章和标签是多对多的关系
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=200, blank=True) #文章摘要
    status = models.CharField(max_length=1,choices=choice)
    like_user = models.ManyToManyField(Likes,verbose_name='点赞人',blank=True,null=True)
    like_num = models.PositiveIntegerField(default=0)
    comment_num = models.PositiveIntegerField(default=0) #取值范围为[0 ,2147483647]
    inspect_num = models.PositiveIntegerField(default=0)

    # 外键关联中 related_name 的用法:
    # 假如 Article 模型里增加一个 users_like 的字段，记录点赞的用户，其与 User 是多对多的关系
    # 我们可以使用 article.users_like.all 查询点赞某篇文章的所有用户，还可以使用 article.users_like.count 来统计某篇文章的总点赞数
    # Article 中 users_like = models.ManyToManyField(User,related_name='articles_liked', blank=True)
    # 通过 user.articles_liked.all 可以查询某个用户所喜欢的所有文章条目(相当于在 User 表中添加了 articles_liked 字段,存储了相关联的 articles)。

    def get_absolute_url(self):
        # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)[source]¶
        # viewname can be a URL pattern name or the callable view object(such as views.archive but not recommend).
        return reverse('myblog:show',kwargs={'article_id': self.id})

    def incre_inspect_num(self):
        self.inspect_num += 1;
        # 这里的 self 是 Article 类的当前实例
        self.save(update_fields=['inspect_num'])

    def incre_comment_num(self):
        self.comment_num += 1;
        # 这里的 self 是 Article 类的当前实例
        self.save(update_fields=['comment_num'])

    def __str__(self):
        return self.article_name

    class Meta:
        ordering = ['-create_time']


