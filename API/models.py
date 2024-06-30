from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from oauth2_provider.models import AccessToken, Application


@receiver(signal=post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        app = Application.objects.create(user=instance, name="api")
        x = app.client_id
        y = app.client_secret
        print(x, y)
        AccessToken.token = "zamalek"
        AccessToken.objects.create(user=instance, application=app, expires="2024-06-29", 
                                   token=AccessToken.token)

        
        