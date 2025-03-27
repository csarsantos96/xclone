from mailersend import EmailClient
from django.http import HttpResponse
from django.conf import settings

def send_test_email(request):
    # Criação do cliente MailerSend
    email_client = EmailClient(api_key=settings.MAILERSEND_API_KEY)

    # Envio de e-mail com o método correto `send()`
    response = email_client.send(
        from_email="contato@cesarsantos.dev",
        to_email="csar.santos18@gmail.com",
        subject="Teste de E-mail",
        text="Este é um e-mail de teste. Verifique se o envio está funcionando corretamente."
    )

    # Imprimir a resposta para debugging
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        return HttpResponse("E-mail de teste enviado com sucesso!")
    else:
        return HttpResponse(f"Erro no envio do e-mail. Status: {response.status_code}, Erro: {response.text}")
