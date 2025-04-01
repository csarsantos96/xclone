from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render


from .email_utils import send_activation_email
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, UserRegisterSerializer
from .utils import (
    send_activation_email,
    decode_token,
    decode_reset_token,
    send_reset_password_email,
)

User = get_user_model()

def send_test_email(request):
    try:
        send_mail(
            'Assunto do Teste',
            'Corpo do email de teste.',
            settings.DEFAULT_FROM_EMAIL,
            ['contato@cesarsantos.dev']
        )
        return HttpResponse("E-mail de teste enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar o e-mail: {str(e)}")




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

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

class CreateUserAPIView(APIView):
    def post(self, request):
        firebase_uid = request.data.get("firebaseUid")
        username = request.data.get("username")
        email = request.data.get("email")

        #
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': username,
            'is_active': True

        })



        return Response({"detail": "Usuário criado/atualizado com sucesso!"}, status=status.HTTP_200_OK)
