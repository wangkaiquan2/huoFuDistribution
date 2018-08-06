import datetime

from django.shortcuts import render, HttpResponse
from django.db import DatabaseError
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import logging
import json

from user.models import User, Limits, Company
from order import models


def index(request):
    """主页"""
    return render(request, 'index.html')


def add_state(request):
    """添加订单壮态列表"""
    # 判断壮态描述与壮态标识是否为空
    if request.POST.get('sname', '') and request.POST.get('state', ''):
        # 判断壮态标识是事存在
        if models.State.objects.filter(state=request.POST['state']):
            result = {'response': '新增壮态标识已存在,请重新输入'}
            return HttpResponse(json.dumps(result))
        else:
            # 新建新的壮态标识
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
    # 序列化壮态信息
    for state in states:
        lstates.append({
            'id': state.id,
            'sname': state.sname,
            'state': state.state
        })
    result = {'response': lstates}
    return render(request, 'inquire_state.html', locals())


def add_order(request):
    """新增订单"""
    # 获取订单相关数据
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
    # 创建订单数据
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
    # 获取当前日期时间
    now = datetime.datetime.now()
    # 获取当日0点
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
    # 获取当日最后一秒
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    # 默认筛选日期
    stime = zeroToday
    etime = lastToday
    # 根据前端日期时间数据筛选
    if request.GET.get('stime', '') and request.GET.get('etime', ''):
        stime = request.GET['stime']
        etime = request.GET['etime']
    orders = models.Order.objects.filter(is_delete=0, ctime__gte=stime, ctime__lte=etime)
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
    paginators = Paginator(orders, 1)
    plist = paginators.page_range
    page_number = 1
    if request.GET.get('page_number', ''):
        page_number = int(request.GET['page_number'])
    try:
        pages = paginators.page(page_number)
    except InvalidPage or PageNotAnInteger or EmptyPage as e:
        logging.warning(e)
        return HttpResponse('无效页码')
    lorder = []
    # 找出订单最后壮态
    for order in pages:
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
    result = {'orders': lorder, 'plist': plist}
    return render(request, 'inquire_order.html', locals())


def inquire_order_state(request):
    """查询订单壮态"""
    order_states = models.Order_State.objects.filter(order_id=request.GET['id'])
    lstates = []
    # 序列化订单壮态
    for order_state in order_states:
        lstates.append({
            'id': order_state.id,
            'ctime': str(order_state.ctime),
            'state': order_state.state.sname
        })
    result = {'response': lstates}
    return render(request, 'inquire_order_state.html', locals())


def modify_orders_state(request):
    """修改订单壮态"""
    orders = request.POST.getlist('orders', '')
    state = request.POST.get('state', '')
    orders_state = []
    x = y = 0
    # 批量修改订单壮态
    for order in orders:
        # 判断订单壮态是否为5且最后一壮态与要添加壮态是否相同
        order_states = models.Order_State.objects.filter(order_id=order)
        if order_states[len(order_states) - 1].state_id == state or order_states.filter(state_id='5'):
            x += 1
        else:
            orders_state.append(models.Order_State(order_id=order, state_id=state))
            y += 1
    models.Order_State.objects.bulk_create(orders_state)
    result = {'response': '重复数据' + str(x) + '条,' + '修改成功' + str(y) + '条'}
    return HttpResponse(json.dumps(result))


def modify_orders_remarks(request):
    """修改订单备注"""
    order = models.Order.objects.get(id=request.POST.get('id', ''))
    # 获取并修改备注信息
    order.remarks = request.POST.get('remarks', '')
    try:
        order.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response': '修改失败'}
        return HttpResponse(json.dumps(result))
    result = {'response': '修改成功'}
    return HttpResponse(json.dumps(result))
