# Spark Vision — Distributed Image Feature Extraction

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-distributed-E25A1C?logo=apachespark&logoColor=white)
![AWS EMR](https://img.shields.io/badge/AWS_EMR-cluster-FF9900?logo=amazonaws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-storage-569A31?logo=amazons3&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-MobileNetV2-FF6F00?logo=tensorflow&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP-blue)

## Présentation du projet

Spark Vision est un MVP de pipeline Computer Vision distribuée pour extraire des caractéristiques visuelles à partir d'images de fruits.

Le projet combine PySpark, TensorFlow, MobileNetV2, AWS EMR et Amazon S3 afin de valider une chaîne de traitement capable de passer d'une exécution locale à une exécution distribuée sur le cloud.

L'objectif n'est pas de livrer une application de classification complète, mais de construire une première base technique robuste pour traiter des volumes d'images plus importants et générer des features exploitables dans une étape de modélisation ultérieure.

## Objectif métier

Le cas d'usage se place dans un contexte AgriTech : préparer une chaîne de traitement d'images de fruits pouvant alimenter, à terme, un moteur de reconnaissance visuelle.

Le besoin principal est de transformer des images brutes en représentations numériques compactes, stockables et réutilisables pour de futurs modèles de classification ou d'analyse.

## Architecture

Le pipeline repose sur quatre blocs principaux :

- Stockage des images dans un dossier local ou dans un bucket Amazon S3.
- Chargement distribué des images avec PySpark au format `binaryFile`.
- Extraction de features via MobileNetV2 pré-entraîné, sans réentraînement du modèle.
- Sauvegarde des résultats au format Parquet pour faciliter la relecture et les traitements ultérieurs.

En local, Spark simule un traitement distribué sur la machine de développement. Sur AWS, EMR fournit un cluster Spark managé, tandis que S3 sert de stockage partagé entre les noeuds du cluster.

## Pipeline technique

Le notebook principal suit les étapes suivantes :

1. Définition des chemins d'entrée et de sortie.
2. Création d'une `SparkSession`.
3. Chargement récursif des images `.jpg`.
4. Extraction du label depuis le chemin de chaque image.
5. Chargement de MobileNetV2 avec les poids ImageNet.
6. Suppression logique de la dernière couche de classification pour récupérer l'avant-dernière couche.
7. Diffusion des poids du modèle aux workers Spark.
8. Prétraitement des images en taille `224x224`.
9. Extraction des vecteurs de caractéristiques avec une pandas UDF.
10. Écriture des features au format Parquet.

Le notebook contient également une étape exploratoire de réduction de dimension par PCA afin d'étudier les features générées.

## Approche Computer Vision

Le projet utilise MobileNetV2 en transfert learning.

Le modèle n'est pas réentraîné : il sert uniquement d'extracteur de caractéristiques. Chaque image est redimensionnée au format attendu par MobileNetV2, puis transformée en vecteur de features issu de l'avant-dernière couche du réseau.

Cette approche permet de produire rapidement des représentations visuelles pertinentes, tout en gardant un pipeline léger pour un premier MVP.

## Déploiement local

Créer un environnement Python, installer les dépendances puis ouvrir le notebook :

```bash
python -m venv .venv
pip install -r requirements.txt -r requirements-dev.txt
jupyter lab
```

Le notebook à exécuter se trouve ici :

```text
notebooks/spark-vision-pipeline.ipynb
```

Pour une exécution locale, les images doivent être placées sous :

```text
data/fruits-360_dataset/fruits-360/Test/
```

Les résultats locaux sont générés dans :

```text
data/Results/
```

Ces dossiers ne sont pas versionnés dans Git afin d'éviter de publier le dataset complet et les artefacts volumineux.

## Déploiement cloud AWS EMR

Le déploiement cloud s'appuie sur :

- Amazon S3 pour stocker les images, le notebook, le script de bootstrap et les résultats Parquet.
- AWS EMR pour exécuter Spark sur un cluster managé.
- JupyterHub pour piloter l'exécution du notebook sur le cluster.
- `bootstrap-emr.sh` pour installer les dépendances Python nécessaires au démarrage du cluster.

La documentation courte de configuration est disponible ici :

```text
docs/aws-emr-setup.md
```

Point important : un cluster EMR est facturé tant qu'il reste actif. Il doit être résilié à la fin de l'exécution pour éviter des coûts inutiles.

## Structure du dépôt

```text
spark-vision/
|-- bootstrap-emr.sh
|-- data/
|   `-- README.md
|-- docs/
|   |-- aws-emr-setup.md
|   `-- spark-vision-presentation.pptx
|-- img/
|   `-- captures AWS, EMR, Spark et MobileNetV2
|-- notebooks/
|   `-- spark-vision-pipeline.ipynb
|-- requirements.txt
`-- requirements-dev.txt
```

## Données et artefacts

Le dataset complet n'est pas inclus dans le dépôt. Les données attendues proviennent du dataset Fruits-360.

Les résultats générés par Spark sont également exclus du versionnement. Ils peuvent être produits localement ou sur S3, puis stockés au format Parquet.

Voir le détail dans :

```text
data/README.md
```

## Résultats

Le pipeline permet de valider :

- le chargement distribué des images avec Spark ;
- l'extraction automatique des labels depuis l'arborescence du dataset ;
- la génération de vecteurs de features MobileNetV2 ;
- la sauvegarde des résultats au format Parquet ;
- l'exécution locale puis cloud sur AWS EMR.

Le notebook montre également une première validation des dimensions de sortie et des visualisations exploratoires autour de la PCA.

## Limites actuelles

Ce projet reste un MVP technique. Il ne contient pas encore :

- d'entraînement supervisé d'un modèle de classification ;
- d'API ou d'interface utilisateur ;
- de pipeline automatisé de bout en bout ;
- de suivi d'expériences ;
- de stratégie avancée d'optimisation des coûts cloud.

Le notebook reste volontairement conservé comme support exploratoire et preuve de démarche.

## Améliorations possibles

Les prochaines étapes naturelles seraient :

- isoler le code du notebook dans des scripts Python réutilisables ;
- ajouter une configuration centralisée des chemins locaux et S3 ;
- entraîner un modèle de classification à partir des features extraites ;
- comparer plusieurs modèles pré-entraînés ;
- suivre les métriques d'exécution Spark et les coûts EMR ;
- automatiser une partie du lancement cloud sans transformer le projet en infrastructure lourde.

## Contexte du projet

Ce projet a été initialement développé dans le cadre d'un parcours professionnalisant en Data Science.

Il est présenté ici comme un MVP technique : une première pipeline distribuée de traitement d'images, structurée autour de PySpark, MobileNetV2, AWS EMR et Amazon S3.
