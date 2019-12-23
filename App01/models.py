from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    is_auther = models.BooleanField(default=False, verbose_name='是否认证')
    phone = models.CharField(max_length=11, verbose_name='电话')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Key(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='开发者', on_delete=models.CASCADE)
    app_name = models.CharField(max_length=10, verbose_name='应用名称')
    key = models.CharField(max_length=32, verbose_name='应用key值')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = 'key表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.key


class Code(models.Model):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    code = models.CharField(max_length=4, verbose_name='验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    end_time = models.DateTimeField(default=datetime.now, verbose_name='过期时间')

    class Meta:
        verbose_name = '验证码表'
        verbose_name_plural = verbose_name
