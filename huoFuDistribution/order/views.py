import datetime

from django.shortcuts import render, HttpResponse
from django.db import DatabaseError
from django.db.models import Q
import logging
import json

from user.models import User, Limits, Company
from order import models


def test(request):
    """测试通迅"""
    return HttpResponse('this is test oreder,is okay')


def add_state(request):
    """添加订单壮态列表"""
    if request.POST.get('sname', '') and request.POST.get('state', ''):
        if models.State.objects.filter(state=request.POST['state']):
            result = {'response': '新增壮态标识已存在,请重新输入'}
            return HttpResponse(json.dumps(result))
        else:
            new_state = models.State(sname=request.POST['sname'], state=request.POST['state'])
            try:
                new_state.save()
            except DatabaseError as e:
                logging.warning(e)
                result = {'response': '新增壮态失败'}
                return HttpResponse(json.dumps(result))
            result = {'response': '新增壮态成功,请刷新'}
            return HttpResponse(json.dumps(result))
    else:
        result = {'response': '壮态标识与壮态描述不能为空'}
        return HttpResponse(json.dumps(result))


def inquire_state(request):
    """查询数据库壮态列表"""
    states = models.State.objects.all()
    lstates = []
    for state in states:
        lstates.append({
            'id': state.id,
            'sname': state.sname,
            'state': state.state
        })
    result = {'response': lstates}
    return HttpResponse(json.dumps(result))


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
    orders = models.Order.objects.filter(is_delete=0)
    now = datetime.datetime.now()
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    stime = zeroToday
    etime = lastToday
    if request.GET.get('stime', '') and request.GET.get('etime', ''):
        stime = request.GET['stime']
        etime = request.GET['etime']
        print('stime:', stime)
        print('etime:', etime)
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
        states = order.order_state_set.all()
        if states:
            state = states[len(states) - 1].state.sname
        else:
            state = '未接单'
        lorder.append({
            'id': order.id,
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
            'state': state,
        })
    result = {'response': lorder}
    return HttpResponse(json.dumps(result))


def modify_orders_state(request):
    """修改订单壮态"""
    orders = request.POST.getlist('orders', '')
    state = request.POST.get('state', '')
    order_states = []
    x = y = 0
    for order in orders:
        if models.Order_State.objects.filter(order_id=order).filter(Q(state_id=state) | Q(state_id='5')).exists():
            x += 1
        else:
            order_states.append(models.Order_State(order_id=order, state_id=state))
            y += 1
    models.Order_State.objects.bulk_create(order_states)
    result = {'response': '重复数据' + str(x) + '条,' + '修改成功' + str(y) + '条'}
    return HttpResponse(json.dumps(result))


