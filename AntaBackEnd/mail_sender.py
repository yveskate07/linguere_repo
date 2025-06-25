import smtplib
from email.message import EmailMessage
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
def mail_to_fablab(user:dict, formation_name=None, reason=None, msg_=None, subject="Demande d'information sur la formation", html_msg=None):

    user_msg = f"Message: {user['message']}" if user.get('message',None) else ""

    msg = EmailMessage()
    if html_msg:
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_msg, 'html'))
        msg["Subject"] = subject

    msg["From"] = sender_email
    msg["To"] = "kateyveschadrac@gmail.com"

    if not reason: # si reason = None alors le mail est envoyé dans le contexte d'une nouvelle inscription à une formation sans plus d'infos (reason)

        # Corps du message professionnel

        if not msg_ and not html_msg: # si le message n'est pas fourni en parametre, on le construit ici directement
            msg["Subject"] = subject + f" {formation_name}"

            corps = f"""\
            Bonjour,
        
            Un utilisateur a manifesté son intérêt pour obtenir davantage d’informations concernant la formation {formation_name}.
            
            Nom: {user['name']}
            Adresse mail: {user['e-mail']}
            Formation: {user['formation']}
            
            {user_msg}
        
            """

        elif msg_: # si le message est fourni en parametre
            corps = msg_
            msg["Subject"] = subject + f" {formation_name}"
            

        if not html_msg: # dans ce cas msg n'est pas un objet MIMEMultipart()
            msg.set_content(corps)

        # Envoi via SMTP sécurisé
        contexte = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
            serveur.login(sender_email, password)
            serveur.send_message(msg)

    else:
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
        msg.set_content(corps)

        # Envoi via SMTP sécurisé
        contexte = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
            serveur.login(sender_email, password)
            serveur.send_message(msg)

# une fonction qui envoie un mail a Linguere fablab indiquant qu'un utilisateur s'est inscrit à tel formation.
def mail_to_the_client(user:dict, formation_name=None, msg_txt=None, subject="Nouvelle inscription pour", html_msg = None):

    msg = EmailMessage()
    if html_msg:
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_msg, 'html'))
        msg['Subject'] = subject
    
    msg["From"] = sender_email
    msg["To"] = user['e-mail']

    # Corps du message professionnel
    #user_msg = f"Message: {user['message']}" if user['message'] else ""

    if not msg_txt and not html_msg:

        msg["Subject"] = subject + f" {formation_name}"
        corps = f"""\
            Bonjour,
    
            Nous avons bien reçu votre inscription pour la formation {formation_name}.
    
            Nous vous contacterons prochainement pour vous fournir plus d'informations.
    
            """

    elif msg_txt:
        msg['Subject'] = subject
        corps = msg_txt

    if not html_msg:
        msg.set_content(corps)

    # Envoi via SMTP sécurisé
    contexte = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
        serveur.login(sender_email, password)
        serveur.send_message(msg)
