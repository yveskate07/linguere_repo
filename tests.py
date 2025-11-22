from django.core.mail import send_mail

def send_test_email():
    send_mail(subject="Test Django",message="Bonjour ! Ceci est un test d'envoi d'email via Django.",from_email="linguerefablab@gmail.com",recipient_list=["katechadrac@gmail.com"],fail_silently=False,)