from django.db import models

# Create your models here.

class Fichier(models.Model):
    fichier_audio = models.FileField(upload_to='audio/')
    # Autres champs de votre modèle

    def __str__(self):
        return self.fichier_audio.name
