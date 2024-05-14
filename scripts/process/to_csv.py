import csv
import os
import spacy
from abbreviations_formated import process_abbreviation_files, extract_long_form_annotations, extract_abbreviation_annotation

"""
Ce script traite des fichiers texte à partir d'un dossier spécifié.
Il utilise SpaCy pour la tokenisation et le POS tagging.
Il utilise des fonctions importées pour le NER tagging.
Plusieurs annotations au niveau du NER tagging sont définies : B-AC (pour les abréviations), B-LF et I-LF (pour les formes longues), B-O (pour tout le reste).
Les annotations et le corpus sont finalement transformés en csv.

Il définit deux fonctions principales :
    - `process_file`
    - `process_directory`


Assurez-vous d'avoir installé les bibliothèques suivantes dans votre environnement Python : 
    - `csv`: Pour manipuler des fichiers csv et générer les résultats
    - `os`: Pour gérer chemins et fichiers.
    - `spacy`: Pour l'analyse linguistique (tokenisation et POS tagging).
    - `abbreviations_formated`: Importation de fonctions contenues dans un autre script pour le NER tagging/reconnaissance des abréviations

Exemple d'utilisation :
    - Définir le chemin `input_directory` pour spécifier le dossier contenant les fichiers texte à traiter.
    - Le fichier de sortie csv contiendra 3 colonnes : tokens, pos_tags, ner_tags
    - Le script peut être exécuté avec une commande simple `python3 to_csv.py`
"""


"""
Le module `abbreviations_formated` fournit des fonctions pour le traitement des abréviations et formes longues.
Il crée un dictionnaire d'annotations et annoter automatiquement un corpus.
Elles sont importées pour constituer la colonne ner_tags du csv et ainsi annoter le corpus en NER.

Fonctions utilisées et importées :
    - `process_abbreviation_files(folder_path)`: Cette fonction parcourt les fichiers texte contenant des abréviations et formes longues puis génère un dictionnaire d'annotations
      associant les abréviations à leurs formes longues correspondantes

    - `extract_long_form_annotations(annotations_dict, long_form)`: Cette fonction extrait les annotations associées à une forme longue spécifique à partir du dictionnaire d'annotations. 
    Elle retourne une liste de tuples contenant les tokens de la forme longue et leurs étiquettes (labels).

    - `extract_abbreviation_annotation(annotations_dict, abbreviation)`: Cette fonction extrait les annotations associées à une abréviation spécifique à partir du dictionnaire d'annotations. 
    Elle retourne une liste de tuples contenant l'abréviation et son étiquette (label).

Importation :
    - Importez les fonctions nécessaires à partir du script `abbreviations_formated`
"""



# Charger le modèle de langue SpaCy pour l'anglais
nlp = spacy.load("en_core_web_sm")

def process_file(file_path, output_writer):
    """
    Cette fonction traite un fichier texte en utilisant SpaCy. Il en fait la tokenisation, le pos tagging et le ner tagging.
    Le ner tagging n'est pas effectué par SpaCy mais par mes propres fonctions de tagging

    Args:
        file_path (str): Chemin du fichier texte à traiter.
        output_writer (csv.writer): Ecrire les résultats dans le fichier csv.

    Returns:
        None (le traitement est écrit dans un fichier csv de sortie)
    """
    # Création du dictionnaire d'annotations à partir des fichiers d'abréviations
    annotations_dict = process_abbreviation_files('../data/abbreviations/abbreviations-clean/')

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        doc = nlp(text)

        for sent in doc.sents:
            # Tokenisation
            tokens = [token.text for token in sent]
            # Annotation des tokens en pos
            pos_tags = [token.pos_ for token in sent]
            ner_tags = []

            # Rechercher les annotations d'abréviation et de forme longue dans la phrase
            sentence_text = ' '.join(tokens)  # Reconstituer les phrases (sinon annotation caduque)
            for token in tokens:
                # Déterminer l'annotation du token (par défaut 'B-O')
                # Si un token n'est ni B-LF, ni I-LF, ni B-AC, il est B-O
                token_annotation = 'B-O'

                # Rechercher si le token correspond à une annotation dans annotations_dict
                for key in annotations_dict.keys():
                    if key in sentence_text and token in key.split():
                        if len(key.split()) > 1:
                            # Il s'agit d'une forme longue
                            key_annotations = extract_long_form_annotations(annotations_dict, key)
                        else:
                            # Il s'agit d'une abréviation
                            key_annotations = extract_abbreviation_annotation(annotations_dict, key)

                        if key_annotations:
                            # Vérifier si le token correspond à une annotation dans le dictionnaire
                            for idx, (ann_token, ann_label) in enumerate(key_annotations):
                                if ann_token == token:
                                    token_annotation = ann_label
                                    break

                # Ajouter l'annotation du token à ner_tags
                ner_tags.append(token_annotation)

            # Écrire les colonnes dans le csv
            output_writer.writerow([tokens, pos_tags, ner_tags])




def process_directory(input_dir, output_file):
    """
    Cette fonction traite tous les fichiers `.txt` d'un dossier donné en appliquant la fonction `process_file` à chacun d'eux
    Les résultats sont écrits dans un fichier csv.

    Args:
        input_dir (str): Dossier contenant les fichiers `.txt` à traiter.
        output_file (str): Chemin du fichier csv de sortie.

    Returns:
        None
    """
    # Ouvrir le fichier csv en écriture
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Création des colonnes comme le corpus PLOD de référence
        csv_writer.writerow(['tokens', 'pos_tags', 'ner_tags'])
        
        # Parcourir tous les fichiers .txt à partir du dossier principal
        for root, dirs, files in os.walk(input_dir):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    process_file(file_path, csv_writer)

input_directory = '../data/clean'

#Fichier csv de sortie
output_csv_file = 'corpus.csv'

process_directory(input_directory, output_csv_file)

print("Traitement terminé. Le fichier .csv a été créé avec succès : ", output_csv_file)
