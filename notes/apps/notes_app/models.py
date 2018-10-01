from django.db import models
from django.conf import settings

#Extend the User Model
# from django.contrib.auth.models import AbstractUser

# class UserProfile(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)

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

class Label(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    label       = models.CharField(primary_key=True, max_length=45)
    labels      = models.ForeignKey('Note', on_delete=models.CASCADE)
    # creaters = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed  = True
        db_table = 'label'
