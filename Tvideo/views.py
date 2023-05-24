from django.shortcuts import render
from .forms import FichierForm
from .models import Fichier
from .utils import transcribe, translate_txt, generate_audio
from django.shortcuts import redirect

def accueil(request):
    return render(request, 'accueil.html')

def resultat(request):
    audio_url = request.GET.get('audio_url')
    fichiers = Fichier.objects.filter(fichier_audio__isnull=False)
    return render(request, 'resultat.html', {'fichiers': fichiers, 'audio_url': audio_url})

from django.shortcuts import redirect
from django.http import QueryDict
from django.urls import reverse

def telechargement_vue(request):
    if request.method == 'POST':
        form = FichierForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            # Enregistrez le fichier ou faites d'autres opérations nécessaires
            texte_traduit = transcribe(fichier)
            text = translate_txt(texte_traduit, "fr")
            # Appliquez le traitement au fichier
            audio = generate_audio(text, "fr", "generated_audio.mp3")

            # Enregistrez l'audio généré dans la base de données
            fichier_obj = Fichier.objects.create(fichier_audio=audio)
            fichier_obj.save()

            # Récupérez l'URL de l'audio généré
            audio_url = fichier_obj.fichier_audio.url

            # Ajoutez l'URL de l'audio généré comme paramètre de requête dans l'URL de redirection
            query_string = QueryDict(mutable=True)
            query_string['audio_url'] = audio_url
            redirect_url = reverse('resultat') + '?' + query_string.urlencode()

            # Redirigez vers la vue resultat avec l'URL de l'audio généré comme paramètre de requête
            return redirect(redirect_url)
    else:
        form = FichierForm()

    return render(request, 'telechargement.html', {'form': form})

