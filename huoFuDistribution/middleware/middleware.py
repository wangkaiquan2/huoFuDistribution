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
                elif path == '/user/update-companys':
                    if self.limits_judgment('3', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/inquire-limits':
                    if self.limits_judgment('4', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/a-inquire-limits':
                    if self.limits_judgment('5', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/add-limits':
                    if self.limits_judgment('6', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/register':
                    if self.limits_judgment('7', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/modify-user':
                    if self.limits_judgment('8', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/inquire-user':
                    if self.limits_judgment('9', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/inquire-user-limit':
                    if self.limits_judgment('10', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/add-user-limits':
                    if self.limits_judgment('11', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/delete-user-limits':
                    if self.limits_judgment('12', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/modify-password':
                    if self.limits_judgment('13', limits):
                        return HttpResponse('权限不足')
                elif path == '/user/quit':
                    if self.limits_judgment('15', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/add-order':
                    if self.limits_judgment('16', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/inquire-order':
                    if self.limits_judgment('17', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/add-state':
                    if self.limits_judgment('18', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/inquire-state':
                    if self.limits_judgment('19', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/modify-orders-state':
                    if self.limits_judgment('20', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/modify-orders-remarks':
                    if self.limits_judgment('21', limits):
                        return HttpResponse('权限不足')
                elif path == '/order/inquire-order-state':
                    if self.limits_judgment('22', limits):
                        return HttpResponse('权限不足')
            else:
                print('重定向')
                return redirect('/user/login')
