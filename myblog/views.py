from django.shortcuts import render,redirect
from comment.forms import CommentForm,LeavingForm,ExpectationForm
from comment.models import Leaving,Expectation
from .models import Article,Category,Tag,User,Likes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse

import markdown

# Create your views here.

def index(request):
    print('首页')
    articles = Article.objects.all()
    context = {'articles':articles}
    print('user_id:',request.user.id)
    print('user_name:',request.user.username)

    # print("Host: ",request.META['HTTP_HOST']) #The HTTP Host header sent by the client.
    # print("Remote_addr: ", request.META['REMOTE_ADDR']) #The IP address of the client
    # print("User_agent: ", request.META['HTTP_USER_AGENT'])  # The client’s user-agent string
    # print("Remote_host: ", request.META['REMOTE_HOST']) #The hostname of the client
    # print("get_host:",request.get_host()) #Returns the originating host of the request,the method uses a combination of SERVER_NAME and SERVER_PORT
    # print("%s: %s" % (request.META['SERVER_NAME'],request.META['SERVER_PORT'])) #The hostname of the server and The port of the server (as a string).
    return render(request,'myblog/index.html',context=context)

def show(request,article_id):
    article = Article.objects.get(pk=article_id)
    theme = article.category
    author_list = User.objects.filter(article=article)
    # 阅读量 +1
    article.incre_inspect_num()
    article.content = markdown.markdown(article.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = article.comment_set.all()
    article.comment_num = len(comment_list)
    article.save(update_fields=['comment_num'])
    article_num = len(Article.objects.all())
    context = {'article': article,
               'author_list':author_list,
               'article_num':article_num,
               'form': form,
               'comment_list': comment_list,
               'theme':theme
               }
    return render(request, 'myblog/show.html', context=context)

@csrf_exempt
def article_like(request):
    '''
    class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None,**kwargs)
    这个类是HttpRespon的子类,第一个参数，data应该是一个字典类型
    如果这样返回，ajax还需要进行json解析

    <views.py>
    return HttpResponse(json.dumps({"msg":"ok!"}))

    <index.html>
    var data=json.parse(data)
    console.log(data.msg);

    如果这样返回，两边都不需要进行json的序列化与反序列化，ajax接受的直接是一个对象
    <views.py>
    from django.http import JsonResponse
    return JsonResponse({"msg":"ok!"})

    <index.html>
    console.log(data.msg);

    :param request:
    :return:
    '''
    if request.method == 'POST':
        # 如果用户表达了喜欢的的类型的话
        action = request.POST.get('action')
        # type = request.POST.get('liketype')
        host_name = request.get_host()
        port = request.get_port()

        http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if http_x_forwarded_for:
            ip_address = http_x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip_address = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

        print("我得到了action:",action)
        print("我得到了hostname:", host_name)
        print("我得到了port:", port)
        print("我得到了ip:", ip_address)
        if action and ip_address:
            try:
                if action == 'article_like':
                    article_id = request.POST.get('id')
                    print("我得到了article_id:", article_id)
                    article = Article.objects.get(pk=article_id)
                    # 相同的 ip 只能在 likes_type 不同的情况下才能存入 Likes 数据库
                    Likes.objects.get_or_create(host_name=host_name, likes_type='article',defaults={'port':port,'ip_address':ip_address})
                    # Q 查询,主要用来表达 "或" 的关系，因为两个条件写在一起表示了 "且" 的逻辑关系
                    user = Likes.objects.get(Q(host_name=host_name)&Q(likes_type='article'))
                    print("user:",user)
                    # print("从点赞人查到的文章集合:",like_user.article_set.all())
                    print('从文章查到的点赞人集合:',article.like_user.all())
                    article_likes = article.like_user.all()
                    if  user not in article_likes:
                        # 一对多不能用 add 而用 = 添加字段值,多对多用 add 添加新的字段值
                        article.like_user.add(user)
                        article.like_num += 1
                        article.save()
                        print("点赞数在数据库更新了")
                    else:
                        return JsonResponse({'status': 'have'})
                elif action == 'person_like':

                    # get_or_create():
                    # Returns a tuple of (object, created), where object is the retrieved or created object
                    # and created is a boolean specifying whether a new object was created.
                    user,created = Likes.objects.get_or_create(host_name=host_name, likes_type='person',defaults={'port': port, 'ip_address': ip_address})

                    # 如果是创建的，就直接返回 "ok" 状态
                    if created:
                        print("点赞数在数据库更新了")
                        return JsonResponse({'status': 'ok'})
                    # 如果不是创建的，说明点赞用户已经在数据库中了，返回 "have" 状态
                    else:
                        return JsonResponse({'status': 'have'})
                return JsonResponse({'status': 'ok'})
            except Likes.DoesNotExist:
                # Likes.objects.create(host_name=host_name, defaults={'port': port, 'ip_address': ip_address})
                print("哦哟，这里异常了！")
    else:
        print("我在这里执行了")
        return JsonResponse({'status': 'fail'})


def nav_category(request,theme):
    print('Category:',theme)
    try:
        category = Category.objects.get(category_name=theme)
        articles = Article.objects.filter(category=category)
        context = {'theme': theme,'article_list':articles}
        return render(request,'myblog/list.html',context=context)
    # If there are no results that match the query, get() will raise a DoesNotExist exception.
    # This exception is an attribute of the model class that the query is being performed on ,
    # if there is no Entry object with a primary key of 1, Django will raise Entry.DoesNotExist.
    except Category.DoseNotExit:
        render(request,'myblog/404.html')


def tools(request):
    print('工具合集')
    return render(request,'myblog/tools.html')

def about(request):
    print('关于自己')
    like_persons = Likes.objects.filter(likes_type='person')
    like_persons_num = len(like_persons)
    context = {'like_persons_num':like_persons_num}
    return render(request,'myblog/about.html',context=context)

def leaving(request):
    print('给我留言')
    leaving_list = Leaving.objects.all()
    leaving_num = len(leaving_list)
    form = LeavingForm()
    context = {'form': form,
               'leaving_list': leaving_list,
               'leaving_num':leaving_num
               }
    return render(request,'myblog/leaving.html',context=context)

def exchange(request):
    print('技术交流')
    return render(request,'myblog/exchange.html')

def spon(request):
    print('赞助作者')
    form = ExpectationForm()
    expectation_list = Expectation.objects.all()
    context = {
        'form': form,
        'expectation_list': expectation_list,
    }
    return render(request,'myblog/spon.html',context=context)

def tag(request,tag_id):
    tag = Tag.objects.get(pk=tag_id)
    articles = Article.objects.filter(tag=tag)
    theme = tag.tag_name+'标签'
    print('tag_name:',theme)
    context = {'article_list':articles,'theme':theme}
    return render(request,'myblog/list.html',context=context)

def archives(request, year, month):
    print("month",month)
    article_list = Article.objects.filter(create_time__year=year).order_by('-create_time')
    num = len(article_list)
    articles = {'article_list': article_list,'num':num,'year':year,'month':month}
    return render(request, 'myblog/list.html', context=articles)

def category(request,category_id):
    category = Category.objects.get(pk=category_id)
    article_list = Article.objects.filter(category=category).order_by('-create_time')
    articles = {'article_list': article_list}
    return render(request, 'myblog/list.html', context=articles)