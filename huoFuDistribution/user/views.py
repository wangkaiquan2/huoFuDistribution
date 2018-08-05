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
        # 获取企业数据
        cnames = request.POST.getlist('cname')
        numbers = request.POST.getlist('number')
        new_companys = []
        x = y = 0
        # 批量创建企业并写入数据库内
        for cname, number in cnames, numbers:
            if cname and number:
                if models.Company.objects.filter(number=number).exists():
                    x += 1
                else:
                    new_companys.append(models.Company(cname=cname, number=number))
                    y += 1
            else:
                x += 1
        models.Company.objects.bulk_create(new_companys)
        result = {'rewponse': '新增企业成功' + str(y) + '条,' + '失败' + str(x) + '条'}
        return HttpResponse(json.dumps(result))


def inquire_companys(request):
    """筛选查询功能"""
    companys = models.Company.objects.all()
    # 根据筛选条件进行关键字包含筛选数据
    if request.GET.get('cname', ''):
        companys = companys.filter(cname__contains=request.GET['cname'])
    if request.GET.get('number', ""):
        companys = companys.filter(number__contains=request.GET['number'])
    if request.GET.get('is_active', ''):
        companys = companys.filter(is_active=request.GET['is_active'])
    lcompanys = []
    # 序列化企业信息
    for company in companys:
        lcompanys.append({
            'id': company.id,
            'cname': company.cname,
            'number': company.number,
            'is_active': company.is_active
        })
    return render(request, 'company.html', locals())


def update_companys(request):
    """修改企业信息"""
    company = models.Company.objects.get(id=request.POST['company_id'])
    # 根据获得的企业信息修改对应的企业信息
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
    llimits = []
    # 序列化权限列表
    for limit in limits:
        llimits.append({
            'id': limit.id,
            'lname': limit.lname,
            'limit': limit.limit
        })
    result = {'response': llimits}
    return render(request, 'inquire_limits.html', locals())


def a_inquire_limits(request):
    """查询功能权限列表"""
    limits = models.Limits.objects.all()
    llimits = []
    # 序列化权限列表
    for limit in limits:
        llimits.append({
            'id': limit.id,
            'lname': limit.lname,
            'limit': limit.limit
        })
    result = {'response': llimits}
    return HttpResponse(json.dumps(result))


def add_limits(request):
    """添加功能权限"""
    # 判断权限描述与权限标识是否为空
    if request.POST.get('lname', '') and request.POST.get('limit', ''):
        # 判断权限标识是否存在
        if not models.Limits.objects.filter(limit=request.POST['limit']):
            # 新增权限
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
        # 判断用户选项是否为空
        if request.POST.get('uname', '') and request.POST.get('password', '') and request.POST.get('company', ''):
            # 判断两次密码是否一致
            if request.POST['password'] == request.POST['password_1']:
                # 判断用户名是否存在
                if not models.User.objects.filter(uname=request.POST['uname']):
                    # 密码加密
                    password = make_password(request.POST['password'], None, 'pbkdf2_sha1')
                    # 新增用户
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
    # 根据前端数据对相应的数据进行更改
    if request.POST.get('password', ''):
        # 密码加密
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
    # 根据前端数据进行相应字段关键字包含筛选
    if request.GET.get('uname', ''):
        users = users.filter(uname__contains=request.GET['uname'])
    if request.GET.get('is_active', ''):
        users = users.filter(is_active=request.GET['is_active'])
    if request.GET.get('company', ''):
        users = users.filter(company__contains=request.GET['company'])
    lusers = []
    for user in users:
        lusers.append({'id': user.id, 'uname': user.uname, 'company': user.company.cname,
                       'is_active': user.is_active, 'ctime': user.ctime})
    return render(request, 'inquire_users.html', locals())


def inquire_user_limit(request):
    """用户权限查询"""
    id = request.GET.get('id', '')
    uname = request.GET.get('uname', '')
    company = request.GET.get('company', '')
    is_active = request.GET.get('is-active', '')
    user = models.User.objects.get(id=id)
    ulimits = user.limits.all()
    limits = []
    # 手动序列化用户权限信息
    for ulimit in ulimits:
        limits.append({'lname': ulimit.lname, 'limit': ulimit.limit})
    return render(request, 'inquire_user_limit.html', locals())


def add_user_limits(request):
    """增加用户权限"""
    if request.method == 'GET':
        return render(request, 'add_user_limits.html')
    else:
        # 判断用户id与权限id是否为空
        if request.POST.get('id', '') and request.POST.get('limits', ''):
            user = models.User.objects.get(id=request.POST['id'])
            # 表与表多对多关系批量增加数据
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
    # 表与表多对多关系，批量移除数据
    user.limits.remove(*request.POST.getlist('limits', ''))
    result = {'response': '删除权限成功'}
    return HttpResponse(json.dumps(result))


def login(request):
    """用户登陆功能"""
    # 判断用户名与密码是否为空
    if request.method == 'GET':
        return render(request,'login.html')
    if request.POST.get('uname', '') and request.POST.get('password', ''):
        user = models.User.objects.filter(uname=request.POST['uname'])
        # 判断用户名是否存在
        if user:
            # 判断密码是否正确
            if check_password(request.POST['password'], user[0].password):
                # 序列化权限列表
                limits = []
                for limit in user[0].limits.all():
                    limits.append(limit.limit)
                    # 将用户id,uname,limits写入session内
                request.session['id'] = user[0].id
                request.session['uname'] = user[0].uname
                request.session['limits'] = limits
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
    # 判断选项是否为空
    if request.POST.get('password', '') and request.POST.get('password_1', '') and request.POST.get('password_2', ''):
        # 判断二次密码是否一致
        if request.POST['password_1'] == request.POST['password_2']:
            user = models.User.objects.get(id=request.session['id'])
            # 判断旧密码是否正确
            if check_password(request.POST['password'], user.password):
                # 新密码加密并修改
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
    # 判断用户是否登陆
    if request.session.get('id', '') and request.session.get('uname', '') and request.session.get('limits', ''):
        # 删除用户登陆相应session
        del request.session['id']
        del request.session['uname']
        del request.session['limits']
        return redirect('/user/login')
    else:
        return redirect('/user/login')
