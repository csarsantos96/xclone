from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Q

from django.shortcuts import render
from django.shortcuts import get_object_or_404

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    print("🔎 Entrou em search_users")
    print("👤 Usuário:", request.user)
    query = request.GET.get('query', '')
    print("📝 Query:", query)

    if query.startswith('@'):
        query = query[1:]

    users = User.objects.filter(
        Q(username__icontains=query) | Q(name__icontains=query)
    )
    print("🔎 Achou usuários:", users)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    current_user = request.user
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "Usuário não encontrado."}, status=404)

    if current_user == target_user:
        return Response({"detail": "Você não pode seguir a si mesmo."}, status=400)

    if target_user in current_user.following.all():
        current_user.following.remove(target_user)
        is_following = False
    else:
        current_user.following.add(target_user)
        is_following = True

    followers_count = target_user.followers.count()

    return Response({
        "is_following": is_following,
        "followers_count": followers_count
    })



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
        name = request.data.get("name", "")

        # Tente buscar o usuário pelo firebase_uid se existir, senão pelo email
        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'is_active': True,
                    'name': name,
                    'firebase_uid': firebase_uid,
                }
            )
            if not created:
                # Se o usuário já existe pelo e-mail, atualize o firebase_uid caso não esteja preenchido
                if not user.firebase_uid:
                    user.firebase_uid = firebase_uid
                user.username = username  # Atualize para o username amigável desejado
                user.name = name
                user.save()
        else:
            # Se o usuário foi encontrado pelo firebase_uid, atualize os dados se necessário
            if user.email != email or user.username != username or user.name != name:
                user.email = email
                user.username = username
                user.name = name
                user.save()

        return Response({"detail": "Usuário criado/atualizado com sucesso!"})


class UserDetailByUsernameAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'username'  # Permite buscar por /users/<username>/

    def get_queryset(self):
        return User.objects.all()


class UserDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'username'  # Ex: /api/accounts/<username>/

    def get_queryset(self):
        return User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        if user_obj != request.user:
            return Response({"detail": "Você não pode editar outro usuário."}, status=403)
        return super().partial_update(request, *args, **kwargs)