from django.db import models
from user.models import Company, User


class State(models.Model):
    """状态"""
    sname = models.CharField('状态名', max_length=18)
    state = models.CharField('状态标识', max_length=3, null=False)

    def __str__(self):
        return self.sname


class Order(models.Model):
    """订单"""
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    # p_order = models.CharField('主单号', max_length=18)
    order_number = models.CharField('订单号', max_length=18, null=False)
    shipper = models.CharField('发货人', max_length=18, null=False)
    quantity = models.IntegerField('数量', default=1)
    weight = models.FloatField('重量', default=0)
    volume = models.FloatField('体积', default=0)
    city = models.CharField('城市', max_length=9, null=False)
    address = models.CharField('地址', max_length=128, null=False)
    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    remarks = models.CharField('备注', max_length=512)
    consignee = models.CharField('收货人', max_length=18, null=False)
    tel = models.CharField('联系方式', max_length=36)
    is_delete = models.BooleanField('是否删除',default=0)

    def __str__(self):
        return self.order_number


class Order_State(models.Model):
    """订单壮态"""
    order = models.ForeignKey(Order)
    state = models.ForeignKey(State)
    ctime = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.state
