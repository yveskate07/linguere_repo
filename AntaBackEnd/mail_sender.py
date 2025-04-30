import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os

load_dotenv()

# Paramètres
sender_email = os.environ["SENDER"]
receiver_email = ""
password = os.environ["PASSWORD"]  # ATTENTION : utilisez un mot de passe d'application ou une méthode plus sécurisée

# Création du message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Sujet de l'e-mail"

body = "Bonjour,\n\nCeci est un e-mail envoyé depuis Python.\n\nCordialement,\nPython"
msg.attach(MIMEText(body, "plain"))

# Connexion au serveur et envoi
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("E-mail envoyé avec succès !")
except Exception as e:
    print(f"Erreur lors de l'envoi : {e}")
