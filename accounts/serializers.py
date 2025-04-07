from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'profile_image', 'cover_image']
        # Mantemos 'id' e 'email' como read_only para evitar alterações indevidas
        read_only_fields = ['id', 'email']

    def validate_username(self, value):
        # Valida se o username começa com '@'
        if not value.startswith('@'):
            raise serializers.ValidationError("O username deve começar com '@'.")
        # Validação via regex para letras, números e underscores
        if not re.match(r'^@[A-Za-z0-9_]+$', value):
            raise serializers.ValidationError(
                "O username deve conter apenas letras, números e underscores, e começar com '@'.")
        return value

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Incluímos também o campo cover_image no registro, se desejado
        fields = ('id', 'name', 'username', 'email', 'password', 'profile_image', 'cover_image')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if not value.startswith('@'):
            raise serializers.ValidationError("O username deve começar com '@'.")
        if not re.match(r'^@[A-Za-z0-9_]+$', value):
            raise serializers.ValidationError(
                "O username deve conter apenas letras, números e underscores, e começar com '@'.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        activation_token = "TOKEN_GERADO_AQUI"
        activation_link = f"http://127.0.0.1:8000/api/accounts/activate/{activation_token}/"
        subject = "Ative sua conta"
        message = f"Olá {user.name}, clique no link para ativar sua conta: {activation_link}"
        user.email_user(subject, message)
