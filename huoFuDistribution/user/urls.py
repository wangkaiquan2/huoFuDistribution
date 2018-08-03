from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^tests/',views.test,name='usertest'),
    url(r'^add-companys/',views.add_company,name='add-company'),
    url(r'^inquire-companys/',views.inquire_companys,name='inquire-companys'),
    url(r'^update-companys/',views.update_companys,name='update-companys'),
    url(r'^inquire-limits/',views.inquire_limits,name='inquire-limits'),
    url(r'^add-limits/',views.add_limits,name='add-limits'),
    url(r'^register/',views.register,name='register'),
    url(r'^modify-user/',views.modify_user,name='modify-user'),
    url(r'^inquire-user/',views.inquire_user,name='inquire-user'),
    url(r'^inquire-user-limit/',views.inquire_user_limit,name='inquire-user-limit'),
    url(r'^add-user-limits/',views.add_user_limits,name='add-user-limits'),
    url(r'^delete-user-limits/',views.delete_user_limits,name='delete-user-limits'),
    url(r'^login/',views.login,name='login'),
    url(r'^modify-password/',views.modify_password,name='modify-password'),
    url(r'^test-session/',views.test_session,name='test-session'),
    url(r'^quit/',views.quit,name='quit'),
]