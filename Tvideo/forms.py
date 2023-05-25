from django import forms


class FichierForm(forms.Form):
    fichier = forms.FileField(label='Fichier')
    choix = forms.ChoiceField(choices=[('audio', 'Audio'), ('video', 'Vidéo')])

class VideoForm(forms.Form):
    fichier_video = forms.FileField(label='Sélectionner une vidéo')
