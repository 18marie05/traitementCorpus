# traitementCorpus
M1 TAL - Outil Traitement de Corpus
---


**PRECISIONS** : Pour ce travail, de constitution de corpus, tout a été réalisé sur la branche `travail` de mon dépôt GitHub, puis tout a été merge sur la branche `main` à la fin.

**STRUCTURE DU DÉPÔT**

Mon dépôt est structuré de cette façon :  

Le dossier **data/** contient :  

- **abbreviations/abbreviations-clean/** et **abbreviations-raw/** qui contiennent les abéviations récupérées pour chaque articles
- **annotated/** qui contient le corpus annoté en ner_tags pour chaque articles
- **clean/** qui est le corpus nettoyé
- **to-scrap/** qui est le dossier des urls principales à scrap
- **corpus.csv** qui est le fichier du corpus au format csv
Le corpus brut **raw/** ne figure pas dans le dossier **data/** car il contenait des fichiers plus volumineux : il est dans le .gitignore. 

Le dossier **notebooks/** contient les notebooks de visualisation des statistiques et de l'ouverture du corpus avec pandas.

Le dossier **script/** contient tous les scripts utilisés pour ce travail.


**Note**
Entre le moment où les scripts ont été écrits afin de constituer le corpus et la fin du travail, des dossiers ont été bougés afin d'obtenir une structure plus claire, mais les chemins dans les scripts n'ont pas été changés.


# Séance 1 - Présentation du corpus 
---

## Tâche à réaliser

La tâche que je souhaite réaliser est une tâche de reconnaissance automatique d'abréviations et de leurs formes longues dans un corpus textuel.  
On se concentre sur un corpus appartenant au vocabulaire médical et scientifique.

## Corpus

Le corpus choisi qui correspond à cette tâche est le corpus PLOD-CW accessible ici : [PLOD-CW dataset](https://huggingface.co/datasets/surrey-nlp/PLOD-CW)  

Ce corpus se concentre sur la reconnaissance d'abréviations dans le contexte médical. Pour cela, il va falloir procéder à la récupération d'articles publiés dans les journaux PLOS, en accès libre.  

Le corpus fait entre 100k et 1M de données. Les créateurs de ce corpus sont : Leonardo Zilio, Hadeel Saadany, Prashant Sharma, Shenbin Qian, Diptesh Kanojia et Constantin Orasan. Il porte uniquement sur de l'anglais.  


## Utilité et modèles

La tâche principale pour laquelle ce corpus peut-être utilisé est le _**token classification**_. Sa sous-tâche est le *ner*, named-entity-recognition.  

Ce corpus est donc utile dans la reconnaissance des abréviations, faisant partie des entités nommées. Le but principal est d'utiliser un corpus technique et médical afin de participer à la reconnaissance de ces abréviations, puis de pouvoir les associer avec leurs formes longues.  

Il a été utilisé pour entraîner différents modèles :  

- roberta-base-finetuned-abbr accessible ici : [Roberta modèle](https://huggingface.co/surrey-nlp/roberta-base-finetuned-abbr)  
- surrey-gp30 accessible ici : [gp30 modèle](https://huggingface.co/cccmatthew/surrey-gp30)  
- roberta-large-finetuned-ner-finetuned-ner accessible ici : [Autre Roberta modèle](https://huggingface.co/EngTig/roberta-large-finetuned-ner-finetuned-ner)  

Les modèles ayant utilisé ce corpus d'entraînement obtiennent des résultats très bons en matière de précision, rappel et F-mesure.  

## A savoir

Dans le NLP, la reconnaissance des abréviations présente un réel challenge. C'est pourquoi ce corpus a été créé. Les journaux PLOS présentent un réel intérêt, puisque dans chaque article, il y a une section *Abbreviations* qui contient l'abréviation et sa forme longue.  

Pour réaliser ce travail et reconstituer ce corpus, on va diminuer la taille du corpus a récupérer. De plus, on va se limiter à 4 catégories du journal PLOS :  

- PLOS Biology
- PLOS Medicine
- PLOS Computational Biology
- PLOS Genetics

Ces catégories sont utilisées dans la constitution du corpus original, c'est pour cette raison que je les ai sélectionnées.  

Le corpus contient 3 colonnes : 

- la phrase tokenisée : colonne *tokens*
- les part-of-speech : colonne *pos_tags*
- les tags d'entités nommées : colonne *ner_tags*


# Séance 2 - Constitution du corpus
---

### Constitution du corpus
Le but est maintenant de récupérer les données dont nous aurons besoin pour constituer le corpus à la même manière que PLOD/CW.  
Pour cela, j'ai effectué plusieurs tentatives avec différents outils : *requests*; *beautifulSoup* et *lxml*.  
Finalement, j'ai décidé d'utiliser les 3 ainsi que *selenium* afin d'effectuer un scraping dynamique.

J'ai commencé par récupérer les 4 liens qui vont servir à récupérer les données textuelles avec `get_links_to_scrap.py` avec *beautifulSoup*, *requests* et *lxml*. Ensuite, j'ai récupéré ses liens pour les scraper avec *selenium* dans le script `scrap_selenium.py`.  
Ce script récupère le contenu textuel de 15 liens pour les différentes catégories sélectionnées puis les stocke dans `data/raw/{category}` où *category* est le nom du dossier pour chaque catégorie.

Ensuite, il faut récupérer les abréviations pour chaque article, si la section est disponible. J'ai réalisé cette tâche avec *selenium* également. Puis, pour chaque catégorie, on récupère 1 fichier dans `data/abbreviations/abbreviations-raw/`. Il va falloir effectuer un traitement supplémentaire avec `clean_abbreviations.py`. Comme il n'y a pas forcément de partie *Abbreviations* pour chaque article, mais qu'elles ne sont pas dans une section particulière, seulement dans une balise *<p>*, il est difficile de les récupérer d'un coup.  
A la fin de ce traitement, il ne reste plus que deux fichiers : *abbreviations_Biology.txt* et *abbreviations_Medicine.txt*. Il n'y avait aucune section *Abbreviations* dans les catégories *Computational Biology* ni *Genetics*. Les résultats sont stockés dans `data/abbreviations/abbreviations-clean/`.  

Ainsi, pour la suite de cette constitution de corpus, nous allons travailler sur les catégories restantes *Medicine* et *Biology*.  

### Nettoyage

Après cette récupération, il faut tout nettoyer car le corpus récupéré est "sale". A l'aide du script `clean_corpus.py`, on va retirer de notre corpus :  

- tout ce qui est dans la partie Figure Citations et toutes les References
- les liens, 
- les patterns du type [ 10 ] ou [ 10 - 13 ] qui sont des renvois vers d'autres liens ou figures, 
- les patterns du type ( Fig 5B and 5C )
- les titres des sections : *Introduction*, *Citations*, *Abstract*  

Cette partie nous a fait perdre trois fichiers : probablement des fichiers mal scrapés ou qui n'avaient pas la même structure que les autres, rendant leur nettoyage non généralisable.  
Le corpus nettoyé se trouve dans `data/clean/`.


### Constitution des NER tags

Après avoir récupérer toutes ces informations, il faut constituer les abréviations avec leurs formes longues.  
Voici un exemple du corpus de référence : la phrase préalablement segmentée *[ "For", "this", "purpose", "the", "Gothenburg", "Young", "Persons", "Empowerment", "Scale", "(", "GYPES", ")", "was", "developed", "." ]* sera annotée *[ "B-O", "B-O", "B-O", "B-O", "B-LF", "I-LF", "I-LF", "I-LF", "I-LF", "B-O", "B-AC", "B-O", "B-O", "B-O", "B-O" ]*.  
Les labems `B-O`, `B-LF`, `I-F` et `B-AC` sont des labels customisés puisqu'ils ne correspondent pas aux labels typiques obtenus lors de processus d'annotation automatique par des outils comme SpaCy par exemple. Les annotations ont été faites avec le schéma BIO.  
Voici les labels : 
**B-LF** correspond à *Begin Long Form*  
**I-LF** correspond à *Inside Long Form*  
**B-AC** correspond à *Begin Abbreviation*  
**B-O** correspond à tous le reste (donc les tokens qui ne sont ni des abréviations, ni des formes longues d'une abréviation).  

Voici les différentes étapes pour parvenir à reconstituer la colonne *ner_tags*.  
Après avoir récupéré et nettoyé les abréviations et leurs formes longues *(comme expliqué dans la partie **Constitution du corpus**)*, j'ai formatté les abréviations afin d'obtenir un dictionnaire dans le script `abbreviations_formated.py`.

Voici un exemple du dictionnaire : 

> `{'ATGL': 'B-AC', 'adipose triglyceride lipase': [{'token': 'adipose', 'label': 'B-LF'}, {'token': 'triglyceride', 'label': 'I-LF'}, {'token': 'lipase', 'label': 'I-LF'}], 'CKD': 'B-AC', 'chronic kidney disease': [{'token': 'chronic', 'label': 'B-LF'}, {'token': 'kidney', 'label': 'I-LF'}, {'token': 'disease', 'label': 'I-LF'}], 'CLEM': 'B-AC', 'correlative light electron microscopy': [{'token': 'correlative', 'label': 'B-LF'}, {'token': 'light', 'label': 'I-LF'}, {'token': 'electron', 'label': 'I-LF'}, {'token': 'microscopy', 'label': 'I-LF'}], 'CNS': 'B-AC', 'central nervous system': [{'token': 'central', 'label': 'B-LF'}, {'token': 'nervous', 'label': 'I-LF'}, {'token': 'system', 'label': 'I-LF'}], 'Cubn': 'B-AC', 'Cubilin': [{'token': 'Cubilin', 'label': 'B-LF'}], 'DGAT1': 'B-AC', 'diglyceride acyltransferase 1': [{'token': 'diglyceride', 'label': 'B-LF'}, {'token': 'acyltransferase', 'label': 'I-LF'}, {'token': '1', 'label': 'I-LF'}]}`

J'ai choisi une méthode de dictionnaire avec le token (abréviation ou forme longue) comme clés et l'annotation BIO en valeur, afin de pouvoir accéder à la valeur en fonction de la clé rencontrée dans le corpus.

Puis dans ce même script, j'ai dû passer par des fonctions intermédiaires avant de passer à la construction du .csv.  

Les fonctions `extract_long_form_annotations()`, `extract_abbreviation_annotation()` et `annotate_files_in_directory()` permettent de récupérer les annotations du dictionnaire et d'annoter le corpus. J'ai choisi de générer des fichiers .txt afin de visualiser plus facilement les annotations pour chaque fichier. Cette fonctionnalité a ensuite été commentée pour réutiliser les fonctions pour construire le csv.



### Constitution du csv

Voici les trois colonnes que je vais reconstituer :  

- la phrase tokenisée : colonne *tokens*
- les part-of-speech : colonne *pos_tags*
- les tags d'entités nommées : colonne *ner_tags*

Pour cela, je crée le script `to_csv.py`. J'utilise spacy pour la tokenisation avec le modèle *en_core_web_sm* pour l'anglais, ainsi que pour l'étiquetage en pos.

La tokenisation et l'étiquetage en pos était simple, puisque ces fonctionnalités sont disponibles dans SpaCy.  

Pour l'annotation en *ner_tags*, c'était plus compliqué puisqu'il ne s'agit pas d'une annotation classique en entités nommées, mais d'une annotation des abréviations et de leurs formes longues.  
L'annotation pour les ner_tags a été réalisée automatiquement sur la base des tokens récupérés dans la partie *Abbreviations*. Il se peut que certains n'aient pas été reconnus s'il n'étaient pas dans la liste.  

Ce script réutilise les fonctions `extract_long_form_annotations()`, `extract_abbreviation_annotation()` et `annotate_files_in_directory()` mentionnés précédemment qui ont été importées.

Le corpus sous forme de .csv se trouve dans `data/clean/corpus-csv/corpus.csv`.  


# Séance 3 - Exploration du corpus
---

Pour cette séance, le but était d'ouvrir et d'explorer notre corpus avec différents outils et de le comparer avec le corpus de référence.  
Pour cela, j'ai utilisé un notebook qui se trouve ici : `notebooks/open_data.ipynb`.  

Maintenant que le corpus est constitué au format csv, j'ai pu tester différents outils : 

- la bibliothèque csv
- la bibliothèque pandas

Le corpus est correctement lu avec les deux bibliothèques mais l'affichage en colonnes mis à disposition par pandas est beaucoup plus lisible : on peut observer correctement les trois colonnes *tokens*, *pos_tags*, *ner_tags*.  

J'ai également pu ouvrir mon corpus avec la librarie `datasets`. On obtient les informations suivantes : 

> `Dataset({features: ['tokens', 'pos_tags', 'ner_tags'], num_rows: 2021})`  

Ensuite, j'ai ouvert mon corpus PLOD/CW de référence :  
> `dataset = load_dataset("surrey-nlp/PLOD-CW", split="train")`

On obtient les informations suivantes :  

> ```Dataset({features: ['tokens', 'pos_tags', 'ner_tags'], num_rows: 1072})```

Consulter ces informations nous permet de voir que les colonnes de mon corpus sont les mêmes que celles présentes dans le corpus de référence.

Lorsqu'on accède aux informations de lignes ou colonnes, on remarque que les types d'informations renvoyées sont également les mêmes : on a bien les tokens dans la colonne `tokens`, les pos_tags dans la colonne `pos_tags` et les ner_tags customisés pour abréviations et formes longues dans la colonne `ner_tags`.  


# Séance 4 - Statistiques et visualisation
---

Pour cette séance, j'ai choisi différentes statistiques que j'ai trouvées pertinentes pour mon corpus.  

J'ai réalisé des statistiques basiques comme la taille des fichiers de mon corpus.  
Puis j'ai voulu inspecter les tokens annotés comme des formes longues et abréviations : il y en a très peu comparé au nombre de tokens qui sont annotés B-O.

Ensuite, j'ai fait la même chose au niveau des POS où la classe *NOUN* est la plus représentée.

Ensuite, j'ai voulu observer la tailles de chaque colonne de mon corpus au format csv. Le but est de savoir si j'ai autant de tokens que de pos_tags que de ner_tags : les listes doivent être de mêmes tailles.  
Le graphique présenté semble montrer un même nombre de ner_tags que de pos_tags, mais pas le même nombre de tokens. Je n'ai pas réussi à comprendre pourquoi.  

Ensuite, j'ai réalisé un graphique avec la Loi de Zipf pour connaître la fréquence des mots de mon corpus.

Pour finir, j'ai décidé de reproduire les statistiques présentées dans le papier de recherche du corpus de référence : un pie plot qui représente la taille des abréviations (en nombre de caractères) et un autre pie plot qui représente la taille des formes longues (en nombre de tokens).  
Le premier graphique a montré que la majorité des abréviations contiennent 3 puis 4 puis 5 caractères.  
Le second a montré que la majorité des formes longues contiennent 3 puis 2 puis 4 tokens.  


