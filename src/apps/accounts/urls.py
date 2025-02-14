from django.urls import path

from .views import authentication_views, studentsdashboards_views

app_name = 'accounts'

urlpatterns = [
    path('authenticate/', authentication_views.AuthenticationView.as_view(), name='authenticate'),
    path('verify_otp/', authentication_views.VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', authentication_views.CustomLogoutView.as_view(), name='logout'),
    
    path('student_dashboards/', studentsdashboards_views.StudentsDashboard.as_view(), name='student_dashboards'),
    path('student_dashboards/edit_profile', studentsdashboards_views.StudentEditProfileView.as_view(), name='student_edit_profile'),
    path('student_dashboards/create-ticket/', studentsdashboards_views.TicketCreateView.as_view(), name='student_create_ticket'),
]
