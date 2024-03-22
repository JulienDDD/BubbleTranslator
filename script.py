from PIL import Image, ImageDraw, ImageFont
import pytesseract
import requests
import textwrap
import io

# Définition de l'api key deepl et du chemin de pytessract
DEEPL_API_KEY = '1fffd358-cc14-2807-1290-f080abcd597d'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Fonction pour extraire le texte d'une image ainsi que les boîtes englobantes de chaque portion de texte détectée.
# @param image: Objet Image PIL à partir duquel le texte sera extrait.
# @return: Dictionnaire contenant les détails du texte extrait et des boîtes englobantes (par exemple, le texte, la position, la largeur, la hauteur).
def extract_text_with_boxes(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    return data

# Fonction pour traduire un texte en utilisant l'API DeepL.
# @param text: Chaîne de caractères représentant le texte à traduire.
# @param target_language: Code de langue (selon la norme ISO 639-1) vers lequel le texte doit être traduit.
# @return: Texte traduit sous forme de chaîne de caractères.
def translate_text(text, target_language='FR'):
    response = requests.post(
        'https://api.deepl.com/v2/translate',
        data={
            'auth_key': DEEPL_API_KEY,
            'text': text,
            'target_lang': target_language
        }
    )
    translated_text = response.json().get('translations')[0].get('text')
    return translated_text

# Fonction pour réintégrer le texte traduit dans l'image originale à l'emplacement des textes originaux.
# @param image_path: Chemin de l'image source dans le système de fichiers.
# @param data: Dictionnaire contenant les informations sur le texte extrait et les boîtes englobantes obtenues de `extract_text_with_boxes`.
# @param target_language: Code de langue cible pour la traduction du texte.
# @return: Chemin de l'image modifiée sauvegardée.
def reintegrate_text(image_path, data, target_language):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("mangat.ttf", 11)

    full_text = ' '.join([d for d in data['text'] if d.strip()])
    translated_text = translate_text(full_text, target_language)  

    original_total_length = sum([len(d) for d in data['text'] if d.strip()])
    translated_length_per_character = len(translated_text) / original_total_length

    current_pos = 0
    for i, segment in enumerate(data['text']):
        if segment.strip():
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            draw.rectangle([x, y, x + w + 19, y + h + 19], fill='white')
            segment_length = len(segment)
            translated_segment_length = int(round(segment_length * translated_length_per_character))
            segment_text = translated_text[current_pos:current_pos + translated_segment_length]

            wrapped_text = textwrap.wrap(segment_text, width=20) 

            for line in wrapped_text:
                draw.text((data['left'][i], data['top'][i]), line, font=font, fill="black")
                data['top'][i] += 14  

            current_pos += translated_segment_length

    output_path = 'translated_image.png'
    image.save(output_path)
    return output_path

# Chemin de l'image source
image_path = 'chaos1.png'

# Charger l'image et extraire le texte avec les boîtes englobantes
image = Image.open(image_path)
data = extract_text_with_boxes(image)

# Réintégrer le texte dans l'image
reintegrate_text(image_path, data, target_language='FR')
