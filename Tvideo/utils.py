from deep_translator import GoogleTranslator
from gtts import gTTS
import numpy as np
import whisper
from django.conf import settings
import os


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
    
    model = whisper.load_model("base")
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
    filepath = os.path.join(settings.STATIC_ROOT, 'audio', generated_audio)
    tts.save(filepath)  
    
    return filepath


