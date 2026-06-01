from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task

@shared_task
def double_nombre(x):
    print(f"Calcul en cours pour {x}")
    return x * 2


@shared_task
def mail_to_fablab(user: dict,subject: str,message_to_admin: str,context: dict | None = None):
    """
    Envoie un mail HTML à Linguere FabLab.
    """

    sender_email = settings.EMAIL_HOST_USER

    ctx = {
        'subject': subject,
        'message_to_admin': message_to_admin,
        'user_message': user.get('message', ''),
    }

    if context:
        ctx.update(context)

    message = render_to_string(
        'Services/mail_for_fablab/index.html',
        ctx
    )

    mail = EmailMessage(
        subject,
        message,
        sender_email,
        to=[user['e-mail']],
        bcc=[user['e-mail'], 'kateyveschadrac@gmail.com']
    )

    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]
    mail.send()

@shared_task
def mail_to_the_client(recipient: str,subject: str,context: dict | None = None):
    """
    Envoie un mail HTML de confirmation au client.
    """

    sender_email = settings.EMAIL_HOST_USER

    ctx = {
        'subject': subject,
    }

    if context:
        ctx.update(context)

    message = render_to_string(
        'Services/mail_for_users/index.html',
        ctx
    )

    mail = EmailMessage(
        subject,
        message,
        sender_email,
        to=[recipient]
    )

    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]
    mail.send()