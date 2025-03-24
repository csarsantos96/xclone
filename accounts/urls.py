# accounts/urls.py

from django.urls import path
from .views import (
    UserRegisterAPIView,
    UserActivateAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('activate/<path:token>/', UserActivateAPIView.as_view(), name='user-activate'),

# Esqueci a senha

    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<path:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
