from django.conf.urls import url
from order import views


urlpatterns = [
    url(r'^test/',views.test,name='test'),
    url(r'^add-order/',views.add_order,name='add-order'),
    url(r'^inquire-order/',views.inquire_order,name='inquire-order'),
    url(r'^add-state/',views.add_state,name='add-state'),
    url(r'^inquire-state/',views.inquire_state,name='inquire-state'),
    url(r'^modify-orders-state/',views.modify_orders_state,name='modify_order_state'),
    url(r'^modify-orders-remarks/',views.modify_orders_remarks,name='modify-orders-remarks'),
    url(r'^inquire-order-state/',views.inquire_order_state,name='inquire-order-state'),
]