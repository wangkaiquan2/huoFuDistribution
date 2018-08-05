from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin


class Limits_judgment(MiddlewareMixin):
    """权限判断类"""

    def limits_judgment(self, limit, limits):
        if limit in limits:
            pass
        else:
            return True

    def process_request(self, request):
        path = request.path
        if path == '/user/login':
            pass
        else:
            if request.session.get('id', ''):
                limits = request.session.get('limits', '')
                if path == '/user/add-companys':
                    if self.limits_judgment('7', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/inquire-companys':
                    if self.limits_judgment('2', limits):
                        return HttpResponse('权限不足')
            else:
                print('重定向')
                return redirect('/user/login')
