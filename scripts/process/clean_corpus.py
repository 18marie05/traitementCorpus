import os
import re

"""
Ce script parcourt de manière récursive tous les fichiers `.txt` à partir d'un dossier principal spécifié dans la variable `dossier`.
Puis il applique plusieurs traitement spécifiques afin de nettoyer ces fichiers.
Les modifications apportées sont écrites dans ces mêmes fichiers.

Voici les les règles de nettoyage :
1. Suppression du contenu entre les sections "Figures Citation" ou "Citation" et "Introduction".
2. Suppression du contenu à partir de la section "References" jusqu'à la fin du fichier.
3. Suppression des liens (urls) présents dans le texte.
4. Suppression des schémas de type `[ 1 – 3 ]`, `[ 1 ]`, `[ 10 ]`, `[ 2 , 3 ]`, `[ 1 ]`.
5. Suppression des schémas de type `( Fig 5B and 5C )`.
6. Suppression des titres des sections comme "Abstract", "Introduction" et "Results".

Assurez-vous d'avoir les modules `os` et `re` dans votre environnement Python.

Exemple d'utilisation :
    - ce script peut être lancé avec la commande simple `python3 clean_corpus.py`

Attention : 
Ce script modifie les fichiers d'origine.
"""


dossier = '../data/clean/'

def nettoyer_fichier(chemin):
    """
    Cette fonction nettoie le contenu d'un fichier en appliquant une série de traitements spécifiques avec le module re.

    Args:
        chemin (str): chemin complet vers les fichiers à nettoyer.

    Returns:
        None (puisque le traitement est écrit dans des fichiers)
    """

    with open(chemin, 'r') as f:
        texte = f.read()

        # Supprimer le contenu entre "Figures Citation" ou "Citation" et "Introduction"
        pattern = r'Figures Citation|Citation'
        match = re.search(pattern, texte)
        debut_suppression = match.start()
        fin_suppression = texte.find('Introduction', debut_suppression)
        texte = texte[:debut_suppression] + texte[fin_suppression:]

        # Supprimer le contenu à partir de "References" jusqu'à la fin
        debut_suppression = texte.find('References')
        texte = texte[:debut_suppression]

        # Supprimer les liens
        texte = re.sub(r'https?://\S+', '', texte)

        # Supprimer les schémas de type [ 1 – 3 ], [ 1 ], [ 10 ], [ 2 , 3 ], [ 1 ]
        texte = re.sub(r'\[(\s?\d+\s?–)+\]', '', texte)
        texte = re.sub(r'\[\d+\]', '', texte)
        texte = re.sub(r'\[(\s?\d+\s?,)+\]', '', texte)
        texte = re.sub(r'\[\s?\d+\s?\]', '', texte)

        # Supprimer les schémas de type ( Fig 5B and 5C )
        texte = re.sub(r'\(.*?Fig.*?\)', '', texte)

        # Supprimer les titres des sections : Abstract Introduction Results
        texte = re.sub(r'Abstract ', '', texte)
        texte = re.sub(r'Introduction ', '', texte)
        texte = re.sub(r'Results ', '', texte)


        # Écrire le texte nettoyé dans le même fichier
        with open(chemin, 'w') as f:
            f.write(texte)

# Parcourir récursivement tous les fichiers .txt à partir du dossier principal
fichiers_trouves = False
for dossier, sous_dossiers, fichiers in os.walk(dossier):
    for nom_fichier in fichiers:
        if nom_fichier.endswith('.txt'):
            chemin_complet = os.path.join(dossier, nom_fichier)
            nettoyer_fichier(chemin_complet)
            print(f"Nettoyage effectué pour {chemin_complet}")
            fichiers_trouves = True

if not fichiers_trouves:
    print(f"Aucun fichier .txt n'a été trouvé dans {dossier} ou ses sous-dossiers")
else:
    print("Nettoyage terminé pour tous les fichiers .txt")