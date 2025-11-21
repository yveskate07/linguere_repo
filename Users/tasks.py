from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from celery import shared_task

@shared_task
def send_verification_email(protocol, domain, user, mail_subject, email_template):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user)
    from_email = settings.EMAIL_HOST_USER
    message = render_to_string(email_template, {
        'user': user,
        'protocol': protocol,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]
    try:
        print("ENVOI DU MAIL...")
        mail.send()
    except Exception as e:
        # Logger l’erreur
        print("Erreur envoi mail : ", e)
    else:
        print("MAIL ENVOYÉ AVEC SUCCES !")


@shared_task
def send_notification(mail_subject, mail_template, context):
    from_email = settings.EMAIL_HOST_USER
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()
