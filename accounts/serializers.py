from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Inclua os campos que desejar, por exemplo:
        fields = ('id', 'name', 'username', 'email', 'password', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if not value.startswith('@'):
            raise serializers.ValidationError("O username deve começar com '@'.")
        # Opcional: Verifica se segue um padrão (somente letras, números, underscores, etc.)
        if not re.match(r'^@[A-Za-z0-9_]+$', value):
            raise serializers.ValidationError(
                "O username deve conter apenas letras, números e underscores, e começar com '@'.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False  # Usuário inativo até a ativação via email
        user.save()
        # Aqui, você pode chamar uma função que envia o email de ativação
        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        # Implemente o envio de email conforme sua lógica:
        # gere um token, construa a URL de ativação e envie o email.
        activation_token = "TOKEN_GERADO_AQUI"  # Exemplo: usando Django's signing ou um JWT
        activation_link = f"http://127.0.0.1:8000/api/accounts/activate/{activation_token}/"
        subject = "Ative sua conta"
        message = f"Olá {user.name}, clique no link para ativar sua conta: {activation_link}"
        user.email_user(subject, message)
