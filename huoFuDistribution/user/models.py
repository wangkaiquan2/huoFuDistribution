from django.db import models


class Company(models.Model):
    """企业表"""
    cname = models.CharField('公司名', max_length=36, null=False)
    number = models.CharField('企业编号', max_length=11, null=False)
    is_active = models.BooleanField('是否启用', default=1)

    def __str__(self):
        return self.cname


class Limits(models.Model):
    """用户权限表"""
    lname = models.CharField('权限描述', max_length=18)
    limit = models.CharField('权限标识', max_length=3, null=False)

    def __str__(self):
        return self.lname


class User(models.Model):
    """用户表"""
    uname = models.CharField('用户名', max_length=18, null=False)
    password = models.CharField('用户密码', max_length=512, null=False)
    is_active = models.BooleanField('是否启用', default=1)
    company = models.ForeignKey(Company)
    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    limits = models.ManyToManyField(Limits)

    def __str__(self):
        return self.uname
