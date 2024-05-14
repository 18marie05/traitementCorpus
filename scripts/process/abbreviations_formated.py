import os

def process_abbreviation_files(folder_path):
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
    # Extraction des annotations des abréviations à partir du dictionnaire
    if abbreviation in annotations_dict:
        label = annotations_dict[abbreviation]
        tokens = [abbreviation]
        annotations = [(token, label) for token in tokens]
        return annotations
    else:
        return None



def annotate_files_in_directory(root_folder, annotations_dict):
    # Parcours des fichiers .txt (corpus)
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Initialiser la liste d'annotations pour le fichier
                annotations = []

                # Comparer le contenu du fichier avec les clés du dictionnaire d'annotations
                for key in annotations_dict.keys():
                    if key in content:
                        # Extraire les annotations pour la clé (forme longue ou abréviation)
                        if len(key.split()) > 1:
                            # Il s'agit d'une forme longue
                            key_annotations = extract_long_form_annotations(annotations_dict, key)
                        else:
                            # Il s'agit d'une abréviation
                            key_annotations = extract_abbreviation_annotation(annotations_dict, key)

                        if key_annotations:
                            annotations.extend(key_annotations)

                return annotations
            
                # Enregistrer les annotations dans un fichier de sortie ou imprimer les résultats
                # Note : cette section est en commentaire cette fonction va être importée en tant que module
                # output_filename = filename.replace('.txt', '_annotated.txt')
                # output_path = os.path.join(root, output_filename)
                # with open(output_path, 'w', encoding='utf-8') as output_file:
                #     for token, label in annotations:
                #         output_file.write(f"{token}\t{label}\n")


corpus_folder = '../data/clean'
annotate_files_in_directory(corpus_folder, annotations_dict)