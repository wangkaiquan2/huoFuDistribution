from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^add-order', views.add_order, name='add-order'),  # 16
    url(r'^inquire-order', views.inquire_order, name='inquire-order'),  # 17
    url(r'^add-state', views.add_state, name='add-state'),  # 18
    url(r'^inquire-state', views.inquire_state, name='inquire-state'),  # 19
    url(r'^modify-orders-state', views.modify_orders_state, name='modify_order_state'),  # 20
    url(r'^modify-orders-remarks', views.modify_orders_remarks, name='modify-orders-remarks'),  # 21
    url(r'^inquire-order-state', views.inquire_order_state, name='inquire-order-state'),  # 22
]
