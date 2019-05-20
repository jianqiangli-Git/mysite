"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('myblog/',include('myblog.urls',namespace='myblog')),
    path('comment/',include('comment.urls',namespace='comment')),
    path('admin/', admin.site.urls),
]

# 将 MEDIA_URL 映射到 MEDIA_ROOT 即将 /media/ 映射到 base_dir + media 类似于 STATIC_URL 可以找到 staic 文件的
# 绝对路径一样(优先查找 STATIC_DIR然后查到 app下的 static)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

