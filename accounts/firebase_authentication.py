from rest_framework import authentication, exceptions
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("🔥 Entrou no FirebaseAuthentication")

        auth_header = request.headers.get('Authorization')
        print("Authorization header:", auth_header)

        if not auth_header or not auth_header.lower().startswith('bearer '):
            print("🚫 Header ausente ou malformado")
            return None

        token = auth_header.split(' ')[1]

        try:
            decoded = firebase_auth.verify_id_token(token)
            print("✅ Token decodificado:", decoded)
        except Exception as e:
            print("❌ Erro na verificação:", e)
            raise exceptions.AuthenticationFailed('Token Firebase inválido')

        uid = decoded.get("uid")
        if not uid:
            raise exceptions.AuthenticationFailed('UID não encontrado no token')

        email = decoded.get("email", "")
        name = decoded.get("name", "")

        User = get_user_model()

        try:
            user = User.objects.get(username=uid)
            print("👤 Usuário encontrado:", user)
        except User.DoesNotExist:
            print("🆕 Criando novo usuário...")
            user = User(username=uid, email=email, name=name)
            user.set_unusable_password()
            user.save()

        print("✅ Autenticado:", user.is_authenticated)
        return (user, None)
