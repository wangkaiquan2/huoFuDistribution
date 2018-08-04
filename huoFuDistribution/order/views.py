from django.shortcuts import render,HttpResponse
from django.db import DatabaseError
import logging
import json

from user.models import User, Limits, Company
from order import models


def test(request):
    """测试通迅"""
    return HttpResponse('this is test oreder,is okay')

    # company = models.ForeignKey(Company)
    # user = models.ForeignKey(User)
    # # p_order = models.CharField('主单号', max_length=18)
    # order_number = models.CharField('订单号', max_length=18, null=False)
    # shipper = models.CharField('发货人', max_length=18, null=False)
    # quantity = models.IntegerField('数量', default=1)
    # weight = models.FloatField('重量', default=0)
    # volume = models.FloatField('体积', default=0)
    # city = models.CharField('城市', max_length=9, null=False)
    # address = models.CharField('地址', max_length=128, null=False)
    # ctime = models.DateTimeField('创建时间', auto_now_add=True)
    # remarks = models.CharField('备注', max_length=512)
    # consignee = models.CharField('收货人', max_length=18, null=False)
    # tel = models.CharField('联系方式', max_length=36)


def add_order(request):
    """新增订单"""
    company = request.POST['company']
    user = request.POST['user']
    order_number = request.POST['order_number']
    shipper = request.POST['shipper']
    quantity = int(request.POST['quantity'])
    weight = float(request.POST['weight'])
    volume = float(request.POST['volume'])
    city = request.POST['city']
    address = request.POST['address']
    remarks = request.POST.get('remarks','')
    consignee = request.POST['consignee']
    tel = request.POST['tel']
    new_order = models.Order(company_id=company,user_id=user,order_number=order_number,shipper=shipper,
                                quantity=quantity,weight=weight,volume=volume,city=city,address=address,
                                remarks=remarks,consignee=consignee,tel=tel)
    try:
        new_order.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response': '提单提交失败'}
        return HttpResponse(json.dumps(result))
    result = {'response': '提单提交成功,请刷新'}
    return HttpResponse(json.dumps(result))