from django.shortcuts import render
from .forms import FichierForm, VideoForm
from .models import Fichier
from .utils import transcribe, translate_txt, generate_audio, generate_video, detect_language
from django.shortcuts import redirect
from django.db.models import Q

def accueil(request):
    return render(request, 'accueil.html')

def resultat(request):
    audio_fichiers = Fichier.objects.filter(fichier_audio__isnull=False)
    video_fichiers = Fichier.objects.filter(fichier_video__isnull=False)
    return render(request, 'resultat.html', {'audio_fichiers': audio_fichiers, 'video_fichiers': video_fichiers})

from django.shortcuts import render

import os

def detect_lang(request):
    if request.method == 'POST':
        # Récupérer le fichier envoyé par le formulaire
        fichier = request.FILES['fichier']
        # Enregistrer le fichier temporaire sur le système de fichiers
        with open('tempfile', 'wb') as temp_file:
            for chunk in fichier.chunks():
                temp_file.write(chunk)
        # Obtenir le chemin du fichier temporaire
        fichier_path = os.path.abspath('tempfile')
        langue_detectee = detect_language(fichier_path)

        # Retourner les résultats ou effectuer une redirection
        return render(request, 'resultats_detect_language.html', {'langue_detectee': langue_detectee})

    return render(request, 'detect_language.html')


def resultats_detect_language(request, resultats):
    return render(request, 'resultats_detect_language.html', {'resultats': resultats})

from django.http import QueryDict
from django.urls import reverse
from django.conf import settings

def telechargement_vue(request):
    if request.method == 'POST':
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            choix = form.cleaned_data['choix']
            langue = form.cleaned_data['langue']  # Récupérer la langue sélectionnée


            if choix == 'audio':
                # Traitement pour le fichier audio
                texte_traduit = transcribe(fichier)
                text = translate_txt(texte_traduit, langue)
                audio = generate_audio(text, langue, "generated_audio.mp3")

                fichier_obj = Fichier.objects.create(fichier_audio=audio)
                fichier_obj.save()

                audio_url = fichier_obj.fichier_audio.url

                query_string = QueryDict(mutable=True)
                query_string['audio_url'] = audio_url
                redirect_url = reverse('resultat') + '?' + query_string.urlencode()

                return redirect(redirect_url)

            elif choix == 'video':
                # Traitement pour le fichier vidéo
                texte_traduit = transcribe(fichier)
                text = translate_txt(texte_traduit, langue)

                # Enregistrer le fichier vidéo sur le disque
                video_path = os.path.join(settings.MEDIA_ROOT, '', fichier.name)
                handle_uploaded_file(fichier, video_path)

                video = generate_video(text, langue, video_path, "generated_video.mp4")

                fichier_obj = Fichier.objects.create(fichier_video=video)
                fichier_obj.save()

                video_url = fichier_obj.fichier_video.url

                query_string = QueryDict(mutable=True)
                query_string['video_url'] = video_url
                redirect_url = reverse('resultat') + '?' + query_string.urlencode()

                return redirect(redirect_url)
    else:
        form = FichierForm()

    return render(request, 'telechargement.html', {'form': form})

def handle_uploaded_file(file, file_path):
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)




