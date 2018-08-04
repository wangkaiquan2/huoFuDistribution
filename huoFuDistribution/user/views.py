from django.shortcuts import render, HttpResponse, redirect
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
    return render(request, 'company.html', locals())


def update_companys(request):
    """修改企业信息"""
    company = models.Company.objects.get(id=request.POST['company_id'])
    if request.POST.get('cname', ''):
        company.cname = request.POST['cname']
    if request.POST.get('number', ''):
        company.number = request.POST['number']
    if request.POST.get('is_active', ''):
        company.is_active = request.POST['is_active']
    try:
        company.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response': '修改异常,请重新操作'}
        return HttpResponse(json.dumps(result))
    result = {'response': '修改成功,请刷新'}
    return HttpResponse(json.dumps(result))


def inquire_limits(request):
    """查询功能权限列表"""
    limits = models.Limits.objects.all()
    return render(request, 'inquire_limits.html', locals())


def add_limits(request):
    """添加功能权限"""
    if request.POST.get('lname', '') and request.POST.get('limit', ''):
        if not models.Limits.objects.filter(limit=request.POST['limit']):
            newLimit = models.Limits(lname=request.POST['lname'], limit=request.POST['limit'])
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
        result = {'response': '权限描述与权限标识不能为空'}
        return HttpResponse(json.dumps(result))


def register(request):
    """用户注册功能"""
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        if request.POST.get('uname', '') and request.POST.get('password', '') and request.POST.get('company', ''):
            if request.POST['password'] == request.POST['password_1']:
                if not models.User.objects.filter(uname=request.POST['uname']):
                    password = make_password(request.POST['password'], None, 'pbkdf2_sha1')
                    newUser = models.User(uname=request.POST['uname'], password=password,
                                          company_id=request.POST['company'])
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


def modify_user(request):
    """用户信息修改"""
    user = models.User.objects.get(id=request.POST.get('id', ''))
    if request.POST.get('password', ''):
        user.password = make_password(request.POST['password'], None, 'pbkdf2_sha1')
    if request.POST.get('is_active', ''):
        user.is_active = request.POST['is_active']
    if request.POST.get('company', ''):
        user.company_id = request.POST['company']
    try:
        user.save()
    except DatabaseError as e:
        logging.warning(e)
        result = {'response': '信息修改失败'}
        return HttpResponse(json.dumps(result))
    result = {'response': '信息修改成功,请刷新'}
    return HttpResponse(json.dumps(result))


def inquire_user(request):
    """用户搜索筛选查询"""
    users = models.User.objects.all()
    if request.GET.get('uname', ''):
        users = users.filter(uname=request.GET['uname'])
    if request.GET.get('is_active', ''):
        users = users.filter(is_active=request.GET['is_active'])
    if request.GET.get('company', ''):
        users = users.filter(company=request.GET['company'])
    # return render(request,'inquire_users.html',locals())
    lusers = []
    for user in users:
        lusers.append({'id': user.id, 'uname': user.uname, 'company': user.company.cname,
                       'is_active': user.is_active, 'ctime': user.ctime})
    return JsonResponse({'users': lusers})


def inquire_user_limit(request):
    """用户权限查询"""
    id = request.GET.get('id', '')
    uname = request.GET.get('uname', '')
    company = request.GET.get('company', '')
    is_active = request.GET.get('is-active', '')
    user = models.User.objects.get(id=id)
    ulimits = user.limits.all()
    limits = []
    for ulimit in ulimits:
        limits.append({'lname': ulimit.lname, 'limit': ulimit.limit})
    return JsonResponse({'id': id, 'uname': uname, 'company': company, 'is_active': is_active, 'ulimits': limits})


def add_user_limits(request):
    """增加用户权限"""
    if request.method == 'GET':
        return render(request, 'add_user_limits.html')
    else:
        if request.POST.get('id', '') and request.POST.get('limits', ''):
            user = models.User.objects.get(id=request.POST['id'])
            print('limits:', request.POST.getlist('limits'))
            try:
                user.limits.add(*request.POST.getlist('limits'))
            except DatabaseError as e:
                logging.warning(e)
                result = {'response': '新增权限失败'}
                return HttpResponse(json.dumps(result))
            result = {'response': '新增权限成功'}
            return HttpResponse(json.dumps(result))
        else:
            result = {'response': '用户名或权限表不能为空'}
            return HttpResponse(json.dumps(result))


def delete_user_limits(request):
    """删除用户权限"""
    user = models.User.objects.get(id=request.POST.get('id', ''))
    print(user)
    user.limits.remove(*request.POST.getlist('limits', ''))
    result = {'response': '删除权限成功'}
    return HttpResponse(json.dumps(result))


def login(request):
    """用户登陆功能"""
    if request.POST.get('uname', '') and request.POST.get('password', ''):
        user = models.User.objects.filter(uname=request.POST['uname'])
        if user:
            if check_password(request.POST['password'], user[0].password):
                limits = []
                for limit in user[0].limits.all():
                    print('limit.limit:', limit.limit)
                    limits.append(limit.limit)
                print('limits:', limits)
                request.session['id'] = user[0].id
                print(user[0].id)
                request.session['uname'] = user[0].uname
                print(user[0].uname)
                request.session['limits'] = limits
                print(limits)
                return render(request, 'index.html')
            else:
                result = {'response': '用户名或密码错误'}
                return HttpResponse(json.dumps(result))
        else:
            result = {'response': '用户不存在'}
            return HttpResponse(json.dumps(result))
    else:
        result = {'response': '用户名或密码不能为空'}
        return HttpResponse(json.dumps(result))


def modify_password(request):
    """修改密码"""
    if request.POST.get('password', '') and request.POST.get('password_1', '') and request.POST.get('password_2', ''):
        if request.POST['password_1'] == request.POST['password_2']:
            user = models.User.objects.get(id=request.session['id'])
            if check_password(request.POST['password'], user.password):
                user.password = make_password(request.POST['password_1'], None, 'pbkdf2_sha1')
                try:
                    user.save()
                except DatabaseError as e:
                    logging.warning(e)
                    result = {'response': '密码修改失败'}
                    return HttpResponse(json.dumps(result))
                result = {'response': '密码修改成功'}
                return HttpResponse(json.dumps(result))
            else:
                result = {'response': '密码错误'}
                return HttpResponse(json.dumps(result))
        else:
            result = {'response': '密码不一致'}
            return HttpResponse(json.dumps(result))
    else:
        result = {'response': '选项不能为空'}
        return HttpResponse(json.dumps(result))


def test_session(request):
    """测试登陆sesson"""
    if request.session.get('id', '') and request.session.get('uname', '') and request.session.get('limits', ''):
        id = request.session['id']
        uname = request.session['uname']
        limits = request.session['limits']
        return JsonResponse({'id': id, 'uname': uname, 'limits': limits})
    else:
        result = {'response': '未登陆'}
        return HttpResponse(json.dumps(result))


def quit(request):
    """用户退出"""
    if request.session.get('id', '') and request.session.get('uname', '') and request.session.get('limits', ''):
        del request.session['id']
        del request.session['uname']
        del request.session['limits']
        return redirect('/user/login')
        # return render(request, 'index.html')
    else:
        return redirect('/user/login')
        # return render(request, 'index.html')
