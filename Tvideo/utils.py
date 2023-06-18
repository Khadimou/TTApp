from deep_translator import GoogleTranslator
from gtts import gTTS
import numpy as np
import whisper
from django.conf import settings
import os

model = None

def load_model():
    global model
    if model is None:
        model = whisper.load_model("tiny")

def detect_language(media):
    load_model()

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(media)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    #print(f"Detected language: {max(probs, key=probs.get)}")

    return max(probs, key=probs.get)


def translate_text(text, lang):
    max_chars = 500
    segments = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    translated_segments = []

    for segment in segments:
        translated_segment = GoogleTranslator(source='auto', target=lang).translate(segment)
        translated_segments.append(translated_segment)

    translated_text = ' '.join(translated_segments)
    return translated_text

def transcribe(path_video):

    load_model()
    result = model.transcribe(path_video.temporary_file_path())
    #with open("trad.txt", "w", encoding="utf-8") as fichier:
        #fichier.write(result["text"])
    return result["text"]


def translate_txt(path_output_txt, lang):
    #contenu = open(path_output_txt, 'r', encoding="utf-8").read()
    # Traduction du texte en utilisant DeepL
    texte_traduit = translate_text(path_output_txt, lang)
    return texte_traduit

def generate_audio(texte_traduit, langue, generated_audio):

    # Génération du fichier audio en utilisant gTTS
    tts = gTTS(text=texte_traduit, lang=langue)
    filepath = os.path.join(settings.MEDIA_ROOT, generated_audio)
    tts.save(filepath)

    return generated_audio

def transcribe_ytb(video_path):
    load_model()
    result = model.transcribe(video_path)
    return result["text"]

def translate_txt_ytb(text, lang):
    texte_traduit = translate_text(text, lang)
    return texte_traduit

from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip
from pytube import YouTube

def generate_video_ytb(texte, langue, fichier_url, video_path):
    # Générer l'audio avec gTTS
    audio_path = os.path.join(settings.MEDIA_ROOT, generate_audio(texte, langue, os.path.join(settings.MEDIA_ROOT, 'translated_audio.mp3')))

    # Télécharger la vidéo à partir de l'URL YouTube
    yt = YouTube(fichier_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    fichier_path = stream.download(output_path='.', filename='tempfile')

    # Charger l'audio et la vidéo d'entrée
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(fichier_path)

    # Ajuster la durée de l'audio à la durée de la vidéo
    audio = audio.set_duration(video.duration)

    # Ajouter l'audio à la vidéo
    video_with_audio = video.set_audio(audio)

    # Déterminer le chemin complet du fichier vidéo généré
    generated_video_path = os.path.join(settings.MEDIA_ROOT, video_path)

    # Sauvegarder la vidéo finale
    video_with_audio.write_videofile(generated_video_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast", ffmpeg_params=["-f", "mp4"])

    return generated_video_path


def generate_video(texte, langue, fichier_video, video_path):
    # Générer l'audio avec gTTS
    audio_path = os.path.join(settings.MEDIA_ROOT,generate_audio(texte, langue, os.path.join(settings.MEDIA_ROOT, 'translated_audio.mp3')))

    # Charger l'audio et la vidéo d'entrée
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(fichier_video)

    # Ajuster la durée de l'audio à la durée de la vidéo
    audio = audio.set_duration(video.duration)

    # Ajouter l'audio à la vidéo
    video_with_audio = video.set_audio(audio)

    # Déterminer le chemin complet du fichier vidéo généré
    generated_video_path = os.path.join(settings.MEDIA_ROOT,video_path)

    # Sauvegarder la vidéo finale
    video_with_audio.write_videofile(generated_video_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast", ffmpeg_params=["-f", "mp4"])

    return generated_video_path