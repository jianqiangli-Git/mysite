# Django 的表单和 orm 不用关注数据库语言的思想类似，正常的前端表单代码应该是像html中那样，但是我们并没有写这些代码，
# 而是写了一个 CommentForm 这个 Python 类。通过调用这个类的一些方法和属性，Django 将自动为我们创建常规的表单代码，

from django import forms
from django.forms import widgets,fields
from .models import Leaving,Expectation,Comment

# 每个Django表单的实例都有一个内置的is_valid()方法，用来验证接收的数据是否合法。如果所有数据都合法，那么该方法将返回True，
# 并将所有的表单数据转存到它的一个叫做 cleaned_data 的属性中，该属性是以个字典类型数据。

from django.db import models
# Create your models here.
# 评论数据库表
class CommentForm(forms.ModelForm):
    class Meta:
        # 表明这个表单对应的数据库模型是 Comment 类
        model = Comment
        fields = ['name',"Email",'text']



class LeavingForm(forms.ModelForm):
    class Meta:
        # 表明这个表单对应的数据库模型是 Leaving 类
        model = Leaving
        fields = ['name',"Email",'text']

class ExpectationForm(forms.ModelForm):
    class Meta:
        # 表明这个表单对应的数据库模型是 Expectation 类
        model = Expectation
        fields = ['name',"Email",'text']