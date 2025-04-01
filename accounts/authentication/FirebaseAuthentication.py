from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth as firebase_auth

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        prefix, token = auth_header.split()
        if prefix.lower() != 'bearer':
            return None

        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        # Pega o uid do Firebase
        uid = decoded.get('uid')
        if not uid:
            raise exceptions.AuthenticationFailed('UID not found in token')

        # Aqui, localiza/cria usuário Django
        # Exemplo:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            user = User.objects.create_user(username=uid)

        return (user, None)
