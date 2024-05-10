# traitementCorpus
M1 TAL - Outil Traitement de Corpus
---


# Séance 1 - Présentation du corpus 
---

## Tâche à réaliser

La tâche que je souhaite réaliser est une tâche de reconnaissance automatique d'abbréviations et de leurs formes longues dans un corpus textuel.  
On se concentre sur un corpus appartenant au vocabulaire médical et scientifique.

## Corpus

Le corpus choisi qui correspond à cette tâche est le corpus PLOD-CW accessible ici : [PLOD-CW dataset](https://huggingface.co/datasets/surrey-nlp/PLOD-CW)  

Ce corpus se concentre sur la reconnaissance d'abbréviations dans le contexte médical. Pour cela, il va falloir procéder à la récupération d'articles publiés dans les journaux PLOS, en accès libre.  

Le corpus fait entre 100k et 1M de données. Les créateurs de ce corpus sont : Leonardo Zilio, Hadeel Saadany, Prashant Sharma, Shenbin Qian, Diptesh Kanojia et Constantin Orasan. Il porte uniquement sur de l'anglais.  


## Utilité et modèles

La tâche principale pour laquelle ce corpus peut-être utilisé est le _**token classification**_. Sa sous-tâche est le *ner*, named-entity-recognition.  

Ce corpus est donc utile dans la reconnaissance des abbréviations, faisant partie des entités nommées. Le but principal est d'utiliser un corpus technique et médical afin de participer à la reconnaissance de ces abbréviations, puis de pouvoir les associer avec leurs formes longues.  

Il a été utilisé pour entraîner différents modèles :  

- roberta-base-finetuned-abbr accessible ici : [Roberta modèle](https://huggingface.co/surrey-nlp/roberta-base-finetuned-abbr)  
- surrey-gp30 accessible ici : [gp30 modèle](https://huggingface.co/cccmatthew/surrey-gp30)  
- roberta-large-finetuned-ner-finetuned-ner accessible ici : [Autre Roberta modèle](https://huggingface.co/EngTig/roberta-large-finetuned-ner-finetuned-ner)  

Les modèles ayant utilisé ce corpus d'entraînement obtiennent des résultats très bons en matière de précision, rappel et F-mesure.  

## A savoir

Dans le NLP, la reconnaissance des abbréviations présente un réel challenge. C'est pourquoi ce corpus a été créé. Les journaux PLOS présentent un réel intérêt, puisque dans chaque article, il y a une section *Abbréviations* qui contient l'abbréviation et sa forme longue.  

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


