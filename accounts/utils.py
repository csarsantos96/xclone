from django.core import signing
from django.core.mail import send_mail
from django.conf import settings


def generate_activation_token(user):
    """
    Gera um token (via django.core.signing) contendo o user_id do usuário.
    """
    data = {"user_id": user.id}
    token = signing.dumps(data)
    return token


def decode_token(token):

    try:
        data = signing.loads(token)
        return data.get("user_id")
    except signing.BadSignature:
        raise ValueError("Token inválido")


def send_activation_email(user):

    token = generate_activation_token(user)
    activation_link = f"http://127.0.0.1:8000/api/accounts/activate/{token}/"

    subject = "Ative sua conta"
    message = (
        f"Olá {user.first_name},\n\n"
        f"Clique no link abaixo para ativar sua conta:\n{activation_link}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
