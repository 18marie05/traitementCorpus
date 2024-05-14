import csv
import os
import spacy
from abbreviations_formated import process_abbreviation_files, extract_long_form_annotations, extract_abbreviation_annotation


# Charger le modèle de langue SpaCy pour l'anglais
nlp = spacy.load("en_core_web_sm")

def process_file(file_path, output_writer):
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
