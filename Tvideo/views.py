from django.shortcuts import render
from .forms import FichierForm, VideoForm
from .models import Fichier
from .utils import transcribe, translate_txt, generate_audio, generate_video
from django.shortcuts import redirect
from django.db.models import Q

def accueil(request):
    return render(request, 'accueil.html')

def resultat(request):
    audio_url = request.GET.get('audio_url')
    fichiers = Fichier.objects.filter(Q(fichier_audio__isnull=False) | Q(fichier_video__isnull=False))
    return render(request, 'resultat.html', {'fichiers': fichiers, 'audio_url': audio_url})


from django.shortcuts import redirect
from django.http import QueryDict
from django.urls import reverse
import os
from django.conf import settings

def telechargement_vue(request):
    if request.method == 'POST':
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            choix = form.cleaned_data['choix']

            if choix == 'audio':
                # Traitement pour le fichier audio
                texte_traduit = transcribe(fichier)
                text = translate_txt(texte_traduit, "fr")
                audio = generate_audio(text, "fr", "generated_audio.mp3")

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
                text = translate_txt(texte_traduit, "fr")

                # Enregistrer le fichier vidéo sur le disque
                video_path = os.path.join(settings.MEDIA_ROOT, '', fichier.name)
                handle_uploaded_file(fichier, video_path)

                video = generate_video(text, "fr", video_path, "generated_video.mp4")

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




