import os
import re

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
