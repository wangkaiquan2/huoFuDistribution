import datetime

from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.db import DatabaseError
import logging
import json
from django.http import JsonResponse

from user import models


def test(request):
    """测试通迅"""
    return HttpResponse('this is test user,okay')


def add_company(request):
    """增加企业"""
    if request.method == 'GET':
        return render(request, 'add_company.html')
    else:
        if request.POST.get('cname', '') and request.POST.get('number', ''):
            if models.Company.objects.filter(number=request.POST['number']):
                result = {'rewponse': '企业编号已被使用'}
                return HttpResponse(json.dumps(result))
            else:
                newCompany = models.Company(cname=request.POST['cname'], number=request.POST['number'])
                try:
                    newCompany.save()
                    result = {'rewponse': '企业新增成功'}
                    return HttpResponse(json.dumps(result))
                except DatabaseError as e:
                    logging.warning(e)
                    result = {'rewponse': '企业新增失败,请重试'}
                    return HttpResponse(json.dumps(result))
        else:
            result = {'response': '企业名或编号不能为空'}
            return HttpResponse(json.dumps(result))


def inquire_order(request):
    """筛选查询功能"""
    companys = models.Company.objects.all()
    if request.GET.get('cname', ''):
        companys = companys.filter(cname=request.GET['cname'])
    if request.GET.get('number', ""):
        companys = companys.filter(number=request.GET['number'])
    if request.GET.get('is_active', ''):
        companys = companys.filter(is_active=request.GET['is_active'])
    # result = {'companys', companys}
    return render(request,'company.html',locals())




def register(request):
    """注册功能"""
    pass
