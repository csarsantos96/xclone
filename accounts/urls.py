from django.urls import path
from .views import (
    UserRegisterAPIView,
    UserActivateAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
    CreateUserAPIView,
    send_test_email
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('activate/<path:token>/', UserActivateAPIView.as_view(), name='user-activate'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<path:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('createUser/', CreateUserAPIView.as_view(), name='create_user'),
path('send-test-email/', send_test_email, name='send_test_email'),
]