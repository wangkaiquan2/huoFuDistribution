from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^test/',views.test,name='usertest'),
    url(r'^add-company/',views.add_company,name='add-company'),
    url(r'^inquire-order/',views.inquire_order,name='inquire-order'),
]