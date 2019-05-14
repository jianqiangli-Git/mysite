from django.db import models
# Create your models here.
# 评论数据库表
class Comment(models.Model):
    name = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255,help_text="请填入你的邮箱")
    # url = models.URLField(blank=True)
    text = models.TextField(blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey('myblog.Article',on_delete=models.CASCADE)  # 一个评论对应一篇文章，文章和评论是一对多的关系

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'


# 留言数据库表
class Leaving(models.Model):
    name = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # user = models.ForeignKey('myblog.User',on_delete=models.CASCADE)
    # GenericIPAddressField:
    # class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)[source]¶
    # An IPv4 or IPv6 address, in string format (e.g. 192.0.2.30 or 2a02:42fe::4). The default form widget(窗口) for this field is a TextInput.
    #
    # The IPv6 address normalization follows RFC 4291#section-2.2 section 2.2, including using the IPv4 format, like ::ffff:192.0.2.0.
    # For example, 2001:0::0:01 would be normalized to 2001::1, and ::ffff:0a0a:0a0a to ::ffff:10.10.10.10. All characters are converted to lowercase.
    #
    # GenericIPAddressField.protocol
    # Limits valid inputs to the specified protocol. Accepted values are 'both' (default), 'IPv4' or 'IPv6'. Matching is case insensitive.
    #
    # GenericIPAddressField.unpack_ipv4
    # Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option is enabled that address would be unpacked to 192.0.2.1. Default is disabled. Can only be used when protocol is set to 'both'.
    #
    # If you allow for blank values, you have to allow for null values since blank values are stored as null.
    # url = models.GenericIPAddressField()

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = '我的留言'
        verbose_name_plural = '我的留言'

class Expectation(models.Model):
    name = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = '我的寄语'
        verbose_name_plural = '我的寄语'