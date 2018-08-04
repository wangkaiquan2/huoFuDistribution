from django.conf.urls import url
from order import views


urlpatterns = [
    url(r'^test/',views.test,name='test'),
    url(r'^add-order/',views.add_order,name='add-order'),
    url(r'^inquire-order/',views.inquire_order,name='inquire-order'),
]