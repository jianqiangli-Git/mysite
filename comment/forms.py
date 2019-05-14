# Django 的表单和 orm 不用关注数据库语言的思想类似，正常的前端表单代码应该是像html中那样，但是我们并没有写这些代码，
# 而是写了一个 CommentForm 这个 Python 类。通过调用这个类的一些方法和属性，Django 将自动为我们创建常规的表单代码，

from django import forms
from .models import Comment,Leaving,Expectation

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