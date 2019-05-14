from django.shortcuts import render,redirect
from myblog.models import Article,User
from .forms import CommentForm,LeavingForm,ExpectationForm
from .models import Leaving,Expectation,Comment
# Create your views here.
# 评论是一个单独的应用

def article_comment(request,article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment-textarea')
        if name and email and comment:
            Comment.objects.create(name=name,Email=email,text=comment,article=article)
            return redirect(article)
        else:
            comment_list = article.comment_set.all()
            context = {'article': article,
                       'comment_list': comment_list
                       }
            return render(request, 'myblog/show.html', context=context)
    else:
        return redirect(article)


# 使用 django Form 表单创建评论提交的表单
# def article_comment(request,article_id):
#     article = Article.objects.get(pk=article_id)
#     if request.method=="POST":
#         # 通过 POST 表单提交的数据实例化 django 表单 CommentForm 类,构造 form 实例
#         form = CommentForm(request.POST)
#
#         if form.is_valid():
#             # 处理 form.cleaned_data 中的数据( subject = form.cleaned_data['subject'] 假如有表单数据库有subject字段)
#             # save() 相当于把存入到数据库中，这里 commit=False 是仅仅利用表单的数据生成 Comment 模型类的实例(即数据库表),但还不保存评论数据到数据库
#             # 如果 commit=False 则 save() 方法返回当前对象，此时也就是 Comment 模型类的实例
#             comment =  form.save(commit=False)
#             # 将数据库表中的 article 字段填上其关联的文章对象(外键)
#             comment.article = article
#             article.incre_comment_num()
#             comment.save()
#             # 如果直接重定向到实例对象,会自动调用 get_absolute_url 方法返回当前对象的 url
#             return redirect(article)
#
#         else:
#             # 反向查询:
#             # Comment和Article是通过ForeignKey关联的，这里article.comment_set.all()也等价于Comment.objects.filter(article=article)，即根据
#             # article 来过滤该article下的全部评论。但既然我们已经有了一个Article模型的实例article(它对应的是Article在数据库中的一条记录),那么获取和
#             # article 关联的评论列表有一个简单方法，即调用它的xxx_set属性来获取一个类似于objects的模型管理器，然后调用其 all 方法来返回这个
#             # article 关联的全部评论.其中 xxx_set 中的 xxx为关联模型的类名(小写).例如 Post.objects.filter(category=cate)也可以等价写为cate.post_set.all()。
#             comment_list = article.comment_set.all()
#             context = {'article': article,
#                        'form': form,
#                        'comment_list': comment_list
#                        }
#             return render(request, 'myblog/show.html', context=context)
#     else:
#         return redirect(article)

# def leaving_comment(request):
#     if request.method=="POST":
#         # 通过 POST 表单提交的数据实例化 django 表单 CommentForm 类,
#         form = LeavingForm(request.POST)
#
#         if form.is_valid():
#             #如果将这实例化的 form 传给前端,将会在前端表单中添加上数据
#             form.save()
#
#             # redirect(to, permanent=False, *args, **kwargs)[source]
#             # Returns an HttpResponseRedirect to the appropriate URL for the arguments passed.
#             #
#             # The arguments could be:
#             #
#             # A model: the model’s get_absolute_url() function will be called.
#             # A view name, possibly with arguments: reverse() will be used to reverse-resolve the name.
#             # (By passing the name of a view and optionally some positional or keyword arguments; the URL will be reverse resolved using the reverse() method)
#             # An absolute or relative URL, which will be used as-is for the redirect location.
#             # By default issues a temporary redirect; pass permanent=True to issue a permanent redirect.
#             # 如果传递 myblog/leaving 将会解析到url:/comment/leaving/myblog/leaving 导致无法匹配 url 的错误
#             # article 的 get_absolute_url 方法为
#             # def get_absolute_url(self):
#             #     return reverse('myblog:show',kwargs={'article_id': self.id})
#             # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)[source]¶
#             # viewname can be a URL pattern name or the callable view object.
#             # 可以看到 url 解析有关的,app 名和 view 名用冒号隔开,直接到某个页面的,用 "/" 隔开
#             return redirect('myblog:leaving')
#
#         else:
#             leaving_list = Leaving.objects.all()
#             context = {
#                        'form': form,
#                        'leaving_list': leaving_list
#                        }
#             return render(request, 'myblog/leaving.html', context=context)
#     else:
#         return redirect('myblog:leaving')

def leaving_comment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment-textarea')
        if name and email and comment:
            Leaving.objects.create(name=name,Email=email,text=comment)
            # 重定向到 views 中的视图函数
            return redirect('myblog:leaving')
        else:
            leaving_list = Leaving.objects.all()
            context = {
                'leaving_list': leaving_list
            }
            return render(request, 'myblog/leaving.html', context=context)
    else:
        return redirect('myblog:leaving')

def expectation_comment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment-textarea')
        if name and email and comment:
            Expectation.objects.create(name=name,Email=email,text=comment)

            # 重定向到 views 中的视图函数
            return redirect('myblog:spon')
        else:
            expectation_list = Expectation.objects.all()
            context = {'comment_list':expectation_list}
            return render(request, 'myblog/show.html', context=context)
    else:
        return redirect('myblog:spon')


# 使用 Form 表单创建 spon 页面下的评论表单
# def expectation_comment(request):
#     if request.method=="POST":
#         # 通过 POST 表单提交的数据实例化 django 表单 CommentForm 类,
#         form = ExpectationForm(request.POST)
#         if form.is_valid():
#             # 如果将这实例化的 form 传给前端,将会在前端表单中添加上数据
#             # 如果写的是 form = NameForm() 则会创建空的表单，就不会填上数据
#             # 通过表单的 is_bound 属性可以获知一个表单已经绑定了数据，还是一个空表，前端的提交按钮需要手动添加！
#             form.save()
#             return redirect('myblog:spon')
#         else:
#             expectation_list = Expectation.objects.all()
#             context = {
#                        'form': form,
#                        'expectation_list': expectation_list
#                        }
#             return render(request, 'myblog/spon.html', context=context)
#     else:
#         return redirect('myblog:spon')

