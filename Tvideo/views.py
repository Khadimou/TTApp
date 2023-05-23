from django.shortcuts import render
from .forms import FichierForm
from .models import Fichier
from .utils import transcribe, translate_txt, generate_audio
from django.http import HttpResponse

def accueil(request):
    return render(request, 'accueil.html')

def resultat(request):
    fichiers = Fichier.objects.all()
    return render(request, 'resultat.html', {'fichiers': fichiers})

def telechargement_vue(request):
    if request.method == 'POST':
        form = FichierForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            fichier = request.FILES['fichier']
            
            # Enregistrez le fichier ou faites d'autres opérations nécessaires
            texte_traduit = transcribe(fichier)
            text = translate_txt(texte_traduit, "fr")
            # Appliquez le traitement au fichier
            fichier_audio = generate_audio(text, "fr", "generated_audio.mp3")
            
            fichier_obj = Fichier()
            fichier_obj.fichier_audio = fichier_audio
            fichier_obj.save()

            # Obtenir l'URL complète du fichier audio
            url = request.build_absolute_uri()

            # Renvoyer la réponse HTTP
            return render(request, 'resultat.html', {'fichiers': [fichier_obj], 'audio_url': url})

    else:
        form = FichierForm()
    return render(request, 'telechargement.html', {'form': form})

