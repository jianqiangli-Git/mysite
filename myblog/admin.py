from django.contrib import admin

# Register your models here.
from .models import Article,Tag,Category,User,Likes
from comment.models import Leaving,Expectation,Comment

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Likes)

admin.site.register(Comment)
admin.site.register(Leaving)
admin.site.register(Expectation)