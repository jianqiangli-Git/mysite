from django.urls import path
from . import views

app_name = 'myblog'

urlpatterns = [
    path('',views.index,name='index'),
    path(r'article/<int:article_id>',views.show,name='show'),
    path(r'article/<int:year>/<int:month>/',views.archives,name='archive'),
    path(r'article/category/<int:category_id>/',views.category,name='category'),
    path(r'article/<str:theme>/',views.nav_category,name='nav_category'),
    path(r'article/tags/<int:tag_id>/',views.tag,name='tag'),
    path(r'article/like',views.article_like,name='like'),
    # path(r'article/<str:category>/<str:theme>/',views.list,name='list'),
    path(r'tools/',views.tools,name='tools'),
    path(r'about/',views.about,name='about'),
    path(r'leaving/',views.leaving,name='leaving'),
    path(r'spon/', views.spon, name='spon'),
    path(r'exchange/',views.exchange,name='exchange'),

]