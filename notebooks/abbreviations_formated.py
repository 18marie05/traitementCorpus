import os

"""
Ce script traite les fichiers d'abréviations en générant des annotations pour les abréviations et les formes longues.
Les annotations sont ensuite faites automatiquement sur un corpus.

Il définit trois fonctions :
    -`process_abbreviation_files()`
    - `extract_long_form_annotations`
    - `extract_abbreviation_annotation`
    - `annotate_files_in_directory`

Exemple d'utilisation :
    - Définir le dossier pour construire le dictionnaire d'annotations (folder_path)
    - Définir le dossier du corpus à annoter (corpus_folder)
    - Le script peut être exécuté avec une commande simple : `python3 abbreviations_formated.py`

Note : Ce script utilise le module `os` pour la gestion des fichiers et des répertoires, ainsi que des expressions
régulières pour le traitement du texte.
"""

def process_abbreviation_files(folder_path):
    """
    Cette fonction génère un dictionnaire d'annotations `annotations_dict` à partir de fichiers `.txt` d'abréviations dans le dossier spécifié.

    Args:
        folder_path (str): chemin du dossier contenant les fichiers d'abréviations.

    Returns:
        dict: dictionnaire d'annotations où les clés sont les abréviations ou les formes longues, et les valeurs sont les annotations correspondantes (B-AC, B-LF, I-LF).
    """
    # Définition du dictionnaire comme variable globale
    global annotations_dict
    # Dictionnaire pour stocker les annotations
    annotations_dict = {}

    # Parcourir les fichiers .txt
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # On sépare le contenu sur ";"
            terms = content.split(';')
            for term in terms:
                # On sépare chaque partie sur ","
                parts = term.split(',')
                if len(parts) >= 2:
                    # La partie 1 est l'abbréviation
                    abbreviation = parts[0].strip()
                    # Le reste est la forme longue associée
                    long_forms = ','.join(parts[1:]).strip()

                    # On sépare la forme longue en tokens
                    lf_tokens = long_forms.split()

                    # Création de l'annotation BIO pour la forme longue
                    # On choisit une liste de dictionnaires
                    # Le premier token de la forme longue est annoté B-LF
                    # Les autres tokens de la forme longue sont annotés I-LF
                    annotated_tokens = [{'token': lf_tokens[0], 'label': 'B-LF'}] + \
                                       [{'token': token, 'label': 'I-LF'} for token in lf_tokens[1:]]

                    # Ajout de l'annotation des abréviations
                    annotations_dict[abbreviation] = 'B-AC'

                    # Ajout des annotations de la forme longue
                    annotations_dict[long_forms] = annotated_tokens
                else:
                    # Gérer le cas où la structure de terme est incorrecte
                    print(f"Terme mal formé ignoré : {term}")

    return annotations_dict



# Utilisation de la fonction pour traiter les fichiers d'abréviations
folder_path = '../data/abbreviations/abbreviations-clean/'
annotations = process_abbreviation_files(folder_path)

print(annotations)


def extract_long_form_annotations(annotations_dict, long_form):
    """
    Cette fonction extrait les annotations des formes longues à partir du dictionnaire d'annotations.

    Args:
        annotations_dict (dict): Dictionnaire d'annotations contenant les informations d'annotation.
        long_form (str): Forme longue pour laquelle on extrait les annotations.

    Returns:
        list: Liste de tuples contenant les tokens et leurs étiquettes (labels) associées.
              Retourne None si la forme longue n'est pas trouvée dans le dictionnaire.
    """
    # Extraction des annotations des formes longues à partir du dictionnaire
    if long_form in annotations_dict:
        annotations = []
        for element in annotations_dict[long_form]:
            if isinstance(element, dict):
                token = element.get('token')
                label = element.get('label')
                if token is not None and label is not None:
                    annotations.append((token, label))
        return annotations
    else:
        return None


def extract_abbreviation_annotation(annotations_dict, abbreviation):
    """
    Cette fonction extrait les annotations des abréviations à partir du dictionnaire d'annotations.

    Args:
        annotations_dict (dict): Dictionnaire d'annotations contenant les informations d'annotation.
        abbreviation (str): Abréviation pour laquelle on extrait les annotations.

    Returns:
        list: Liste de tuples contenant les tokens (abréviations) et leur étiquette (label) associée.
              Retourne None si l'abréviation n'est pas trouvée dans le dictionnaire.
    """
    # Extraction des annotations des abréviations à partir du dictionnaire
    if abbreviation in annotations_dict:
        label = annotations_dict[abbreviation]
        tokens = [abbreviation]
        annotations = [(token, label) for token in tokens]
        return annotations
    else:
        return None



def annotate_files_in_directory(root_folder, annotations_dict):
    """
    Applique les annotations extraites du dictionnaire aux fichiers `.txt` d'un répertoire spécifié.

    Args:
        root_folder (str): Répertoire contenant les fichiers `.txt` à annoter.
        annotations_dict (dict): Dictionnaire d'annotations contenant les informations d'annotation.

    Returns:
        None (Les fichiers annotés sont sauvegardés individuellement).
    """
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Initialiser la liste d'annotations pour le fichier
                annotations = []

                # Parcourir les termes du dictionnaire d'annotations
                for key in annotations_dict.keys():
                    if key in content:
                        if len(key.split()) > 1:
                            # Il s'agit d'une forme longue
                            key_annotations = extract_long_form_annotations(annotations_dict, key)
                        else:
                            # Il s'agit d'une abréviation
                            key_annotations = extract_abbreviation_annotation(annotations_dict, key)

                        if key_annotations:
                            annotations.extend(key_annotations)

                # Créer un fichier de sortie annoté pour chaque fichier du corpus
                # Fonctionnalité commentée
                # output_filename = filename.replace('.txt', '_annotated.txt')
                # output_path = os.path.join(root, output_filename)
                # with open(output_path, 'w', encoding='utf-8') as output_file:
                #     # Parcourir le contenu du fichier original et écrire les annotations
                #     tokens = content.split()
                #     for token in tokens:
                #         found_annotation = False
                #         for ann_token, label in annotations:
                #             if token == ann_token:
                #                 output_file.write(f"{token}\t{label}\n")
                #                 found_annotation = True
                #                 break
                #         if not found_annotation:
                #             output_file.write(f"{token}\tB-O\n")

                return annotations

# Exemple d'utilisation
corpus_folder = '../data/clean'
annotate_files_in_directory(corpus_folder, annotations_dict)
