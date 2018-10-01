from django.contrib import admin

#Extending the USER model for future use
from .models import Note, Label


# Register your models here.
admin.site.register(Note)
admin.site.register(Label)
