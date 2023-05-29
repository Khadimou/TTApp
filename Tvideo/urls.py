from django.urls import path
from Tvideo import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),  # URL pattern pour la page d'accueil
    path('telechargement/', views.telechargement_vue, name='telechargement'),
    path('resultat/', views.resultat, name='resultat'),
    path('detect_lang/', views.detect_lang, name='detect_lang'),
    path('resultats_detect_language/<str:resultats>/', views.resultats_detect_language, name='resultats_detect_language'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
