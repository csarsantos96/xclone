from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

def send_activation_email(user, request):
    """
    Gera o token de ativação e envia para o email do usuário.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode('utf-8')).decode()
    domain = get_current_site(request).domain
    activation_link = f'http://{domain}/api/accounts/activate/{uid}/{token}/'

    subject = "Ative sua conta"
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(
        subject,
        message,
        'no-reply@yourdomain.com',
        [user.email],
        fail_silently=False,
    )
