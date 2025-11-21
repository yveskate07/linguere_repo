from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# une fonction qui envoie un mail a Linguere Fablab
@shared_task
def mail_to_fablab(user:dict, is_formation=True , admin_edit_view='' ,formation_name=None, reason='new inscription'):
    """
    fonction qui envoie un mail a Linguere Fablab soit pour :
    1. une nouvelle inscription a une formation avec msg du client, reason='new inscription' 
    2. une demande de contact avec msg du client, reason='information request'
    3. informer que quelqu'un a téléchargé une brochure, reason='new pdf downloaded'
    4. informer que quelqu'un a passé une nouvelle commande de service, reason='new service order'
    """

    # encryptage de admin_edit_view

    data = {"new inscription":{
                               "subject":"Nouvelle inscription", 
                               'message_to_admin':f"Un utilisateur vient de s'inscrire à la formation {formation_name}.", 
                               "user_message":user["message"], 
                               "link":admin_edit_view},
            "information request":{
                                "subject":'Demande d\'information pour la formation', 
                                'message_to_admin':f"Un utilisateur a demandé des informations concernant la formation {formation_name}.", 
                                "user_message":user["message"], 
                                "link":admin_edit_view},
            "new pdf downloaded":{
                                "subject":'Nouvelle brochure téléchargée pour la formation', 
                                'message_to_admin':f"Un utilisateur a téléchargé la brochure pour la formation {formation_name}.", 
                                "user_message":user["message"], 
                                "link":admin_edit_view},
            "new service order":{
                                "subject":'Nouvelle commande de service enregistrée', 
                                'message_to_admin':f"Un utilisateur a passé une commande de service. Le service est : {formation_name}.", 
                                "user_message":user["message"], 
                                "link":admin_edit_view}
            }
    
    context = {
                'subject': data[reason]['subject'],
               'message_to_admin':data[reason]['message_to_admin'],
               'user_message':None if not is_formation else data[reason]['user_message'],
               'link':data[reason]['link']
               }

    sender_email = settings.EMAIL_HOST_USER

    message = render_to_string('Services/mail_for_fablab/index.html', context)

    mail = EmailMessage(data[reason]['subject'], message, sender_email, to=[user['e-mail']])
    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]
    mail.send()


# une fonction qui envoie un mail a Linguere fablab indiquant qu'un utilisateur s'est inscrit à tel formation.
@shared_task
def mail_to_the_client(user:dict, is_formation, formation_name=None, context = None):

    """
    fonction qui envoie un mail a l'utilisateur lorsque:
    1. il s'inscrit a une formation, formation_name doit etre renseigné
    2. il passe une commande de service, subject doit etre adapté
    """
    sender_email = settings.EMAIL_HOST_USER
    ctx={'subject':f'Votre inscription a été enregistrée pour la formation {formation_name} !' if not is_formation else f'Votre commande a été enregistrée pour le service {formation_name}!', 
             'is_order':not is_formation, 
             'success_msg_for_signup':"Votre inscription à la formation a été enregistrée avec succès. Nous vous contacterons prochainement avec plus de détails."
             }
    
    if context:
        ctx.update(context)
    
    message=render_to_string('Services/mail_for_users/index.html', ctx)

    mail = EmailMessage(ctx['subject'], message, sender_email, to=[user['e-mail']])
    mail.content_subtype = "html"
    mail.reply_to = [settings.DEFAULT_FROM_EMAIL]

    mail.send()