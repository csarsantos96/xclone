from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'name', 'username', 'email',
            'profile_image', 'cover_image',
            'following_count', 'followers_count',
        ]
        ...

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

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
