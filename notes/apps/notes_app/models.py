from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#Using the Auth_User Model as user

#Create a token for every new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Note(models.Model):
    title       = models.CharField(max_length=45, blank=False, null=True)
    note        = models.CharField(max_length=500, blank=False, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    notes       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed  = True
        db_table = 'note'

    def __str__(self):
        return str(self.title)

    @property
    def owner(self):
        return self.notes

class Label(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    label       = models.CharField(primary_key=True, max_length=45)
    labels      = models.ForeignKey('Note', on_delete=models.CASCADE)
    # creaters = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed  = True
        db_table = 'label'
