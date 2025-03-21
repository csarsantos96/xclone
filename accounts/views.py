from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Importamos do utils.py (sem importar de volta para lá)
from .utils import send_activation_email, decode_token

User = get_user_model()

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Cria o usuário inicialmente inativo, envia e-mail com token de ativação.
        """
        user = serializer.save(is_active=False)
        send_activation_email(user)


class UserActivateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        """
        Endpoint que recebe o token na URL e ativa a conta se o token for válido.
        """
        try:
            user_id = decode_token(token)
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Token inválido."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"detail": "Conta ativada com sucesso!"},
                        status=status.HTTP_200_OK)
