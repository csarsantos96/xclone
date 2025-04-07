from django.urls import path
from .views import (
    UserRegisterAPIView,
    UserActivateAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
    CreateUserAPIView,
    send_test_email,
    get_current_user,
    update_profile,
    UserDetailUpdateAPIView,
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('activate/<path:token>/', UserActivateAPIView.as_view(), name='user-activate'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<path:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('createUser/', CreateUserAPIView.as_view(), name='create_user'),
    path('me/', get_current_user, name='get_current_user'),
    path('update/', update_profile, name='update_profile'),
    # Rota unificada para GET e PATCH:
    path('<str:username>/', UserDetailUpdateAPIView.as_view(), name='user-detail-update'),
    path('send-test-email/', send_test_email, name='send_test_email'),
]
