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


def inquire_companys(request):
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


def update_companys(request):
    """修改企业信息"""
    company = models.Company.objects.get(id=request.POST['company_id'])
    if request.POST.get('cname',''):
        company.cname = request.POST['cname']
    if request.POST.get('number',''):
        company.number = request.POST['number']
    if request.POST.get('is_active',''):
        company.is_active = request.POST['is_active']
    try:
        company.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response':'修改异常,请重新操作'}
        return HttpResponse(json.dumps(result))
    result = {'response': '修改成功,请刷新'}
    return HttpResponse(json.dumps(result))


def inquire_limits(request):
    """查询功能权限列表"""
    limits = models.Limits.objects.all()
    return render(request,'inquire_limits.html',locals())


def add_limits(request):
    """添加功能权限"""
    if request.POST.get('lname','') and request.POST.get('limit',''):
        if not models.Limits.objects.filter(limit=request.POST['limit']):
            newLimit = models.Limits(lname=request.POST['lname'],limit=request.POST['limit'])
            try:
                newLimit.save()
            except DatabaseError as e:
                logging.warning(e)
                result = {'response': '添加权限未知异常'}
                return HttpResponse(json.dumps(result))
            result = {'response': '添加权限成功'}
            return HttpResponse(json.dumps(result))

        else:
            result = {'response': '权限标识已存在'}
            return HttpResponse(json.dumps(result))
    else:
        result = {'response':'权限描述与权限标识不能为空'}
        return HttpResponse(json.dumps(result))


def register(request):
    """用户注册功能"""
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        if request.POST.get('uname','') and request.POST.get('password','') and request.POST.get('company',''):
            if request.POST['password'] == request.POST['password_1']:
                if not models.User.objects.filter(uname=request.POST['uname']):
                    password = make_password(request.POST['password'],None,'pbkdf2_sha1')
                    newUser = models.User(uname=request.POST['uname'],password=password,company_id=request.POST['company'])
                    try:
                        newUser.save()
                    except DatabaseError as e:
                        logging.warning(e)
                        result = {'response': '注册用户失败'}
                        return HttpResponse(json.dumps(result))
                    result = {'response': '注册用户成功'}
                    return HttpResponse(json.dumps(result))
                else:
                    result = {'response': '用户名已存在'}
                    return HttpResponse(json.dumps(result))
            else:
                result = {'response': '密码不一致,请重新输入'}
                return HttpResponse(json.dumps(result))
        else:
            result = {'response': '用户名、密码、企业不能为空'}
            return HttpResponse(json.dumps(result))
