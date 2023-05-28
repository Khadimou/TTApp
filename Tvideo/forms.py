from django import forms

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'Anglais'),
    ('es', 'Espagnol'),
    ('ar', 'Arabe'),
    ('bn', 'Bengali'),
    ('ru', 'Russe'),
    ('pt', 'Portugais'),
    ('id', 'Indonésien'),
    ('ur', 'Urdu'),
    ('de', 'Allemand'),
    ('ja', 'Japonais'),
    ('sw', 'Swahili (Kiswahili)'),
    ('mr', 'Marathi'),
    ('te', 'Telugu'),
    ('ta', 'Tamil'),
    ('tr', 'Turc'),
    ('ko', 'Coréen (du Sud)'),
    ('vi', 'Vietnamien (du Nord)'),
    ('it', 'Italien'),
    ('yo', 'Yoruba (Nigeria)'),
    ('gu', 'Gujarati (Inde)'),
    ('jv', 'Javanais (Indonésie)'),
    ('kn', 'Kannada (Inde)'),
    ('fa', 'Persan (Iran)'),
    ('bho', 'Bhojpuri (Inde)'),
    ('hak', 'Hakka (Chine)'),
    ('uk', 'Ukrainien'),
    ('hsn', 'Xiang (Chine)'),
    ('ml', 'Malayalam (Inde)'),
    ('uz', 'Ouzbekistan'),
    ('sd', 'Sindhi (Pakistan)'),
    ('am', 'Amharique (Éthiopie)'),
    ('ps', 'Farsi / Persan '),
    ('tl', 'Tagalog / Filipino '),
    ('pl', 'Polonais'),
    ('swc', 'Swahili '),
    ('sh', 'Serbe / Croate / Bosnien'),
    ('ne', 'Népalais')
]


class FichierForm(forms.Form):
    fichier = forms.FileField(label='Fichier')
    choix = forms.ChoiceField(choices=[('audio', 'Audio'), ('video', 'Vidéo')])
    langue = forms.ChoiceField(choices=LANGUAGES, label='Langue de traduction')

class VideoForm(forms.Form):
    fichier_video = forms.FileField(label='Sélectionner une vidéo')
