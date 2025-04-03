from django.urls import path

from .views import order_view, peyment_view

app_name = 'orders'

urlpatterns = [
    path('', order_view.OrderCreateView.as_view(), name='order_create',),

    path('zp_process/', peyment_view.payment_process, name='zp_payment_process'),
    path('zp_callback/', peyment_view.payment_callback, name='zp_payment_callback'),
]
