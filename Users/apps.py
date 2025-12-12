from django.apps import AppConfig
print("signals.py bien chargé")

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'
    verbose_name = 'Utilisateurs'

def ready(self):
    from Users import signals
