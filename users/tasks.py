import os

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_email(url: str, email: str) -> None:

    send_mail(
        subject='Account Activation',
        message=f'To activate your account, follow the link {url}',
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
    )
