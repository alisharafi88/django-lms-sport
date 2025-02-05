from django.urls import path

from . import views

app_name = 'carts'
urlpatterns = [
    path('', views.cart_view, name='cart',),
    path('add/<int:course_id>/', views.add_to_cart_view, name='cart_add'),
    path('remove/<int:course_id>/', views.remove_course_view, name='cart_remove'),
    path('clear/', views.clear_cart_view, name='cart_clear'),
]

