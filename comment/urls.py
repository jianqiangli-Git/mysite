from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path(r'article/<int:article_id>',views.article_comment,name='article_comment'),
    path(r'leaving/',views.leaving_comment,name='leaving_comment'),
    path(r'expectation/',views.expectation_comment,name='expectation_comment')
]