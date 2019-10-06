from django.urls import path, include
from rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView)
from rest_auth.registration.views import RegisterView


app_name = 'jobs_auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('password/change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('password/reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
]
