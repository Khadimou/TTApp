from django import forms

class FichierForm(forms.Form):
    """ champ1 = forms.CharField(label='Champ 1', max_length=100)
    champ2 = forms.IntegerField(label='Champ 2')
    champ3 = forms.EmailField(label='Champ 3') """
    fichier = forms.FileField(label='Fichier')
