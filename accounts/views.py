import jwt
from django.http import HttpResponse
from mailersend import EmailClient
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer, UserRegisterSerializer
from .utils import send_activation_email, decode_token, send_reset_password_email

User = get_user_model()

from mailersend import EmailClient

def send_test_email(request):
    # Criação do cliente MailerSend
    email_client = EmailClient()

    # Envio de e-mail
    response = email_client.send_email(
        from_email="contato@cesarsantos.dev",
        to_email="csar.santos18@gmail.com",
        subject="Teste de E-mail",
        text="Este é um e-mail de teste. Verifique se o envio está funcionando corretamente."
    )

    # Imprimir a resposta completa para debugging
    print(response.text)
    print(response.status_code)

    if response.status_code == 200:
        return HttpResponse("E-mail de teste enviado com sucesso!")
    else:
        return HttpResponse(f"Erro no envio do e-mail. Status: {response.status_code}, Erro: {response.text}")




# Função para gerar o token de ativação
def generate_activation_token(user):
    """Gera um token para ativação do usuário"""
    payload = {'user_id': user.id}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


# View para o registro de usuário
class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"detail": "Campos obrigatórios faltando."}, status=status.HTTP_400_BAD_REQUEST)

        # Cria o usuário no banco de dados com is_active=False (não ativado)
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)

        # Gera o token de ativação
        activation_token = generate_activation_token(user)

        # URL para a página de ativação (substitua com a URL real do frontend)
        activation_url = f"http://localhost:3000/activate/{activation_token}"  # Aqui você pode configurar a URL real
        subject = "Ative sua conta"
        message = render_to_string('activation_email.html', {
            'user': user,
            'activation_url': activation_url,
        })

        # Envia o e-mail de ativação
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # Resposta de sucesso, informando o frontend que o email de ativação foi enviado
        return Response({
            "detail": "Usuário registrado com sucesso! Verifique seu e-mail para ativar sua conta."
        }, status=status.HTTP_201_CREATED)



# View para ativação da conta do usuário
class UserActivateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            # Decodifica o token e verifica se o usuário existe
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token expirado."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Ativa a conta do usuário
        user.is_active = True
        user.save()

        return Response({"detail": "Conta ativada com sucesso!"}, status=status.HTTP_200_OK)


# View para atualização do perfil do usuário
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# View para redefinir a senha
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


# View para redefinir a senha do usuário
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


# View para criar usuário (Firebase + Django)
class CreateUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        firebase_uid = request.data.get("firebaseUid")
        username = request.data.get("username")
        email = request.data.get("email")

        if not firebase_uid or not username or not email:
            return Response({"detail": "Campos obrigatórios faltando."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email, defaults={
            'username': username,
            'is_active': True
        })

        if not created:
            return Response({"detail": "Este e-mail já está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Usuário criado/atualizado com sucesso!"}, status=status.HTTP_200_OK)
