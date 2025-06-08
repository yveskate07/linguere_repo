import smtplib
from email.message import EmailMessage
import ssl
from pathlib import Path
import AntaBackEnd.settings as settings
from dotenv import load_dotenv
import os

load_dotenv()

# Paramètres
sender_email = os.environ["SENDER"]
password = os.environ["PASSWORD"]  # ATTENTION : utilisez un mot de passe d'application ou une méthode plus sécurisée

# une fonction qui envoie un mail a l'utilisateur qui a demandé la brochure
def brochure_to_client_through_mail(receiver_email, formation_name, user:dict, reason='téléchargeant une brochure', msg_=None):
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"Brochure {formation_name}"

    # Corps du message
    corps = f"""\
    Bonjour,

    Veuillez trouver ci-joint la brochure pour la formation {formation_name}.

    N'hésitez pas à revenir vers nous pour toute information complémentaire.

    Cordialement,
    Linguere FabLab.
    """
    msg.set_content(corps)

    chemin_pdf = settings.BASE_DIR / 'Formations' / 'static' / 'Formations' / 'brochures' / formation_name / 'brochure.pdf'

    # Lecture et ajout du fichier PDF
    with open(chemin_pdf, 'rb') as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=chemin_pdf.split("/")[-1])

    # Envoi via un serveur SMTP (exemple avec Gmail)
    contexte = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexte) as serveur:
        serveur.login(sender_email, password)
        serveur.send_message(msg)

        mail_to_fablab(formation_name=formation_name, user=user, reason=reason, msg_=msg_)

# une fonction qui envoie un mail a Linguere Fablab avec la requete de l'utilisateur voulant prendre contact
def mail_to_fablab(user:dict, formation_name=None, reason=None, msg_=None, subject="Demande d'information sur la formation"):

    user_msg = f"Message: {user['message']}" if user['message'] else ""

    if not reason:
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = sender_email


        # Corps du message professionnel

        if not msg:
            msg["Subject"] = subject + f" {formation_name}"

            corps = f"""\
            Bonjour,
        
            Un utilisateur a manifesté son intérêt pour obtenir davantage d’informations concernant la formation {formation_name}.
            
            Nom: {user['name']}
            Adresse mail: {user['e-mail']}
            Formation: {user['formation']}
            
            {user_msg}
        
            """

        else:
            corps = msg

        msg.set_content(corps)

        # Envoi via SMTP sécurisé
        contexte = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
            serveur.login(sender_email, password)
            serveur.send_message(msg)
            #print("Notification envoyée avec succès.")

    else:
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = sender_email
        msg["Subject"] = "Demande d'information sur la formation"

        # Corps du message professionnel
        corps = f"""\
                Bonjour,

                Un utilisateur a manifesté son intérêt pour obtenir davantage d’informations concernant la formation {formation_name} en {reason}.

                Nom: {user['name']}
                Adresse mail: {user['e-mail']}
                Formation: {user['formation']}
                
                {user_msg}

                """
        # {"Message: " + msg_ if msg_ else ''}
        msg.set_content(corps)

        # Envoi via SMTP sécurisé
        contexte = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
            serveur.login(sender_email, password)
            serveur.send_message(msg)
            # print("Notification envoyée avec succès.")

# une fonction qui envoie un mail a Linguere fablab indiquant qu'un utilisateur s'est inscrit à tel formation.
def mail_to_the_client(user:dict, formation_name=None, msg=None, subject="Nouvelle inscription pour"):

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = user['e-mail']

    # Corps du message professionnel
    user_msg = f"Message: {user['message']}" if user['message'] else ""

    if not msg:

        msg["Subject"] = subject + f" {formation_name}"
        corps = f"""\
            Bonjour,
    
            Nous avons bien reçu votre inscription pour la formation {formation_name}.
    
            Nous vous contacterons prochainement pour vous fournir plus d'informations.
    
            """

    else:
        corps = msg

    msg.set_content(corps)

    # Envoi via SMTP sécurisé
    contexte = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
        serveur.login(sender_email, password)
        serveur.send_message(msg)
