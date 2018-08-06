from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^add-companys', views.add_company, name='add-company'),  # 1
    url(r'^inquire-companys', views.inquire_companys, name='inquire-companys'),  # 2
    url(r'^update-companys', views.update_companys, name='update-companys'),  # 3
    url(r'^inquire-limits', views.inquire_limits, name='inquire-limits'),  # 4
    url(r'^a-inquire-limits', views.a_inquire_limits, name='a-inquire-limits'),  # 5
    url(r'^add-limits', views.add_limits, name='add-limits'),  # 6
    url(r'^register', views.register, name='register'),  # 7
    url(r'^modify-user', views.modify_user, name='modify-user'),  # 8
    url(r'^inquire-users', views.inquire_user, name='inquire-users'),  # 9
    url(r'^inquire-user-limits', views.inquire_user_limit, name='inquire-user-limits'),  # 10
    url(r'^add-user-limits', views.add_user_limits, name='add-user-limits'),  # 11
    url(r'^delete-user-limits', views.delete_user_limits, name='delete-user-limits'),  # 12
    url(r'^login', views.login, name='login'),
    url(r'^modify-password', views.modify_password, name='modify-password'),  # 13
    url(r'^test-session', views.test_session, name='test-session'),  # 14
    url(r'^quit', views.quit, name='quit'),  # 15
]
