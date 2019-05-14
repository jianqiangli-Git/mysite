from django import template
from ..models import Category,Article,Tag
from django.db.models.aggregates import Count

register = template.Library()
# Library.filter(name,function,is_safe=False,needs_autoescape=False,excepts_localtime=False)
# 函数默认需要两个参数，name是装饰器的名称(字符串类型)，function是函数名。
# register.filter('truncate_chars',truncate_chars)
# def truncate_chars(value):
#     if value.__len__() > 30:
#         return '%s......'% value[0:30]
#     else:
#         return value
# 也可以通过装饰器进行登记:
# @register.filter(name='truncate_filter')
# def truncate_chars(value):
#     if value.__len__() > 30:
#         return '%s......'% value[0:30]
#     else:
#         return value
# 如果没有使用name参数，django默认会将函数名作为name参数的值，所以下面的代码和上面的代码作用相同。
# @register.filter
# def truncate_chars(value):
#     if value.__len__() > 30:
#         return '%s......'% value[0:30]
#     else:
#         return value
# 自定义模板过滤器(filter)
@register.filter(name='div_5')
def div(x):
    return x%5+1

# 自定义模板标签
@register.simple_tag(name='categorys')
def get_categorys():
    return Category.objects.all()

# dates 方法返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 Python 的 date 对象，其有一个 year 和 month 属性。精确到月份，降序排列。
# 接受三个参数 created_time 创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）
@register.simple_tag(name='date_archive')
def archive():
    return Article.objects.dates('create_time','month',order='DESC')

@register.simple_tag(name='categorys')
def get_categorys():
    # Count(在 django.db.models.aggregates 中引入) 计算分类下的文章数,其接受的参数为需要计数的模型的名称,它接收一个和 Categoty 相关联的模型参数名
    # (这里是 Post，通过 ForeignKey 关联的)然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中
    # 这里 annotate 做的事情就是把全部 Category 取出来，然后去 Post 查询每一个 Category 对应的文章，查询完成后只需算一下每个 category id 对应有多少行记录，
    # 这样就可以统计出每个 Category 下有多少篇文章了。现在在 Category 列表中每一项都新增了一个 num_posts 属性记录该 Category 下的文章数量，
    # 我们就可以在模板中直接引用这个属性来显示分类下的文章数量了(注意是给每个Category实例增加了num_posts属性，但并未在数据库中增加这个属性)。
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

@register.simple_tag
def get_tags():
    # 标签云
    # annotate:注释,注解
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

@register.simple_tag(name='most_comment_articles')
def get_most_comment_article(num=8):
    return Article.objects.all().order_by('-comment_num')[:num]