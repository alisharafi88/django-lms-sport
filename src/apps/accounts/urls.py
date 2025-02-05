from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('authenticate/', views.AuthenticationView.as_view(), name='authenticate'),
    path('verify_otp/', views.VerifyOTPView.as_view(), name='verify_otp')
]
