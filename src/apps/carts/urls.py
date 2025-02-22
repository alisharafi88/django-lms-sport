from django.urls import path

from . import views

app_name = 'carts'
urlpatterns = [
    path('', views.cart_view, name='cart',),
    path('add/<int:product_id>/<str:product_type>/', views.add_to_cart_view, name='cart_add'),
    path('remove/<int:product_id>/<str:product_type>/', views.remove_from_cart_view, name='cart_remove'),
    path('clear/', views.clear_cart_view, name='cart_clear'),
]

