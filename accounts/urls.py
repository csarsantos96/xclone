# accounts/urls.py

from django.urls import path
from .views import UserRegisterAPIView, UserActivateAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('activate/<path:token>/', UserActivateAPIView.as_view(), name='user-activate'),
]
