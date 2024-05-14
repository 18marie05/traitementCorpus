import os
import re


"""
Ce script traite les fichiers d'abréviations bruts (dossier abbreviations-raw) en filtrant les lignes qui commencent par "Abbreviations". 
Puis, il crée de nouveaux fichiers nettoyés (dossier abbreviations-clean) contenant uniquement ces lignes.

Le script parcourt un répertoire contenant des fichiers d'abréviations au format texte (.txt).
Si une ligne commence par "Abbreviations", elles sont gardées.
Les nouveaux fichiers contenant ces lignes sont sauvegardés dans un répertoire spécifié dans la variable `clean_directory`.

Exemple d'utilisation :
    - Le script peut être lancé avec la commande simple `python3 clean_abbreviations.py`
    - Les fichiers générés sont enregistrés dans `data/abbreviations/abbreviations-clean` directement. Aucune création de dossier n'est nécessaire au préalable

Assureé-vous d'avoir les paquets suivant dans votre environnement python : 
    - os pour manipuler les fichiers et arborescences
    - re pour manipuler des expressions régulières

"""


# Chemin pour les fichiers raw et clean des abbréviations
raw_directory = 'data/abbreviations/abbreviations-raw'
clean_directory = 'data/abbreviations/abbreviations-clean'

if not os.path.exists(clean_directory):
    os.makedirs(clean_directory)

# Pour chaque fichier du dossier raw
for filename in os.listdir(raw_directory):
    if filename.endswith('.txt'):
        raw_filepath = os.path.join(raw_directory, filename)
        
        # Lire le contenu de chaque fichier .txt
        with open(raw_filepath, 'r') as raw_file:
            lines = raw_file.readlines()
            
            # Regarder si la ligne commence par "Abbreviations"
            has_abbreviations = any(re.match(r'^Abbreviations', line) for line in lines)
            
            if has_abbreviations:
                clean_filepath = os.path.join(clean_directory, filename)
                
                # Si oui, on conserve uniquement ces lignes, tout le reste est supprimé
                with open(clean_filepath, 'w') as clean_file:
                    filtered_lines = [line for line in lines if re.match(r'^Abbreviations', line)]
                    clean_file.writelines(filtered_lines)
                    
                    print(f"Fichier nettoyé '{filename}' créé à '{clean_directory}'.")
            else:
                print(f"Aucune ligne ne commence par'Abbreviations' dans '{filename}'. Aucun nouveau fichier n'a été créé.")
