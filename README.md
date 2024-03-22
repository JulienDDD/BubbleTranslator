
# Bubble translator

Ce script permet d'extraire le texte d'une image avec fond blanc (bulle), de le traduire dans la langue souhaitée en utilisant l'API DeepL, puis de réintégrer le texte traduit à l'emplacement original dans l'image.

## Fonctionnalités

- Extraction de texte et des boîtes englobantes à partir d'images.
- Traduction du texte extrait via l'API DeepL.
- Réintégration du texte traduit dans l'image originale.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé Python 3 et les paquets suivants :

- PIL (Pillow)
- pytesseract
- requests

Vous aurez également besoin de :

- Une clé API DeepL valide.
- Tesseract OCR installé sur votre machine.

## Installation

1. Installez Python 3 si ce n'est pas déjà fait.
2. Installez Tesseract OCR. Suivez les instructions sur [le site officiel de Tesseract](https://github.com/tesseract-ocr/tesseract/wiki) pour votre système d'exploitation.
3. Installez les dépendances Python en exécutant :

```bash
pip install Pillow pytesseract requests
```

4. Clonez ce dépôt ou téléchargez le script directement.

## Configuration

1. Ouvrez le script dans un éditeur de texte.
2. Remplacez la valeur de `DEEPL_API_KEY` par votre clé API DeepL personnelle.

## Utilisation

Pour utiliser ce script, vous devez avoir une image contenant du texte que vous souhaitez traduire. Le script est configuré pour traduire le texte en français, mais vous pouvez modifier la langue cible en changeant le paramètre `target_language` dans la fonction `translate_text` et `reintegrate_text`.

Exemple d'utilisation :

```python
# Chemin de votre image
image_path = 'chemin/vers/votre/image.png'

# Charger l'image et extraire le texte avec les boîtes englobantes
image = Image.open(image_path)
data = extract_text_with_boxes(image)

# Réintégrer le texte dans l'image
reintegrate_text(image_path, data, target_language='FR')
```

## Licence

Ce projet est sous licence MIT. Veuillez voir le fichier LICENSE pour plus de détails.
