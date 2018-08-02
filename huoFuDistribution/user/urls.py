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
    url(r'^inquire-user/',views.inquire_user,name='inquire-user'),
]