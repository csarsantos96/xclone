from rest_framework import generics, permissions, status

from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .utils import (
    send_activation_email,
    decode_token,
    decode_reset_token,
    send_reset_password_email,
)

User = get_user_model()

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        send_activation_email(user)


class UserActivateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            user_id = decode_token(token)
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"detail": "Conta ativada com sucesso!"}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"detail": "E-mail é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Se este e-mail existir, enviaremos um link de redefinição."})

        # Envia e-mail com o link de redefinição
        send_reset_password_email(user)
        return Response({"detail": "Verifique seu e-mail para redefinir a senha."})



class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response(
                {"detail": "Preencha 'new_password' e 'confirm_password'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"detail": "As senhas não conferem."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = decode_reset_token(token)
            user = User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            return Response(
                {"detail": "Token inválido ou usuário não encontrado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Senha redefinida com sucesso!"}, status=status.HTTP_200_OK)