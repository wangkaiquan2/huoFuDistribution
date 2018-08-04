import datetime

from django.shortcuts import render, HttpResponse
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
    remarks = request.POST.get('remarks', '')
    consignee = request.POST['consignee']
    tel = request.POST['tel']
    new_order = models.Order(company_id=company, user_id=user, order_number=order_number, shipper=shipper,
                             quantity=quantity, weight=weight, volume=volume, city=city, address=address,
                             remarks=remarks, consignee=consignee, tel=tel)
    try:
        new_order.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response': '提单提交失败'}
        return HttpResponse(json.dumps(result))
    result = {'response': '提单提交成功,请刷新'}
    return HttpResponse(json.dumps(result))


def inquire_order(request):
    """查询订单"""
    orders = models.Order.objects.all()
    now = datetime.datetime.now()
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    stime = zeroToday
    etime = lastToday
    if request.GET.get('stime', '') and request.GET.get('etime', ''):
        stime = request.GET['stime']
        etime = request.GET['etime']
        print('stime:',stime)
        print('etime:',etime)
    orders = orders.filter(ctime__gte=stime).filter(ctime__lte=etime)
    if request.GET.get('order_number', ''):
        orders = orders.filter(order_number=request.GET['order_number'])
    if request.GET.get('shipper', ''):
        orders = orders.filter(shipper=request.GET['shipper'])
    if request.GET.get('quantity', ''):
        orders = orders.filter(quantity=request.GET['quantity'])
    if request.GET.get('weight', ''):
        orders = orders.filter(weight=request.GET['weight'])
    if request.GET.get('volume', ''):
        orders = orders.filter(volume=request.GET['volume'])
    if request.GET.get('city', ''):
        orders = orders.filter(city=request.GET['city'])
    if request.GET.get('consignee', ''):
        orders = orders.filter(consignee=request.GET['consignee'])
    if request.GET.get('tel', ''):
        orders = orders.filter(tel=request.GET['tel'])
    if request.GET.get('remarks', ''):
        orders = orders.filter(remarks=request.GET['remarks'])
    lorder = []
    for order in orders:
        lorder.append({
            'company': order.company_id,
            'user': order.user_id,
            'order_number': order.order_number,
            'shipper': order.shipper,
            'quantity': order.quantity,
            'weight': order.weight,
            'volume': order.volume,
            'city': order.city,
            'address': order.address,
            'ctime': str(order.ctime),
            'remarks': order.remarks,
            'consignee': order.consignee,
            'tel': order.tel,
        })
    result = {'response': lorder}
    return HttpResponse(json.dumps(result))
