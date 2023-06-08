from django.db import models

# Create your models here.

class Fichier(models.Model):
    fichier_audio = models.FileField(upload_to='media/', null=True, blank=True)
    fichier_video = models.FileField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f"Fichier #{self.id}"
