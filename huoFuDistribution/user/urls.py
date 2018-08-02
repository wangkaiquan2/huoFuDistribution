from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^tests/',views.test,name='usertest'),
    url(r'^add-companys/',views.add_company,name='add-company'),
    url(r'^inquire-companys/',views.inquire_companys,name='inquire-companys'),
    url(r'^update-companys/',views.update_companys,name='update-companys'),
]