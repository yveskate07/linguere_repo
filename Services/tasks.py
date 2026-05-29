from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def double_nombre(x):
    print(f"Calcul en cours pour {x}")    # On simule une petite tâche
    return x * 2


# une fonction qui envoie un mail a Linguere Fablab
@shared_task
def mail_to_fablab(msg):
    """
    fonction qui envoie un mail a Linguere Fablab pour informer qu'une nouvelle commande a été enregistrée.
    """

    sender_email = settings.EMAIL_HOST_USER

    mail = EmailMessage(subject="Nouvelle commande de service enregistrée", body=msg, from_email=sender_email, to=[sender_email])
    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]
    mail.send()


# une fonction qui envoie un mail a Linguere fablab indiquant qu'un utilisateur s'est inscrit à tel formation.
@shared_task
def mail_to_the_client(user_email, msg):

    """
    fonction qui envoie un mail a l'utilisateur lorsqu'il passe une commande de service, subject doit etre adapté
    """
    sender_email = settings.EMAIL_HOST_USER

    mail = EmailMessage(subject="Votre commande a été enregistrée", body=msg, from_email=sender_email, to=[user_email])
    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]

    mail.send()