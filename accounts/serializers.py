from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import CustomUser



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'profile_image']

        def validate_bio(self, value):
            if len(value) > 140:
                raise serializers.ValidationError("A bio não pode exceder 140 caracteres.")
            return value


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
