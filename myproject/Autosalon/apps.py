from django.apps import AppConfig

class AutosalonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Autosalon'
    
    # def ready(self):
    #     import Autosalon.signals