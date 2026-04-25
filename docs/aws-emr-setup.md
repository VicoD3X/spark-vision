# Configuration AWS EMR et S3

Ce document résume la configuration cloud utilisée par le projet. Il complète le notebook sans remplacer les captures présentes dans `img/`.

## Rôle de S3

Amazon S3 sert de stockage central pour le pipeline.

Il contient :

- les images d'entrée du dataset Fruits-360 ;
- le notebook exécuté depuis l'environnement EMR/JupyterHub ;
- le script `bootstrap-emr.sh` ;
- les résultats générés par Spark au format Parquet.

Dans le notebook, les chemins cloud suivent le principe suivant :

```python
PATH = "s3://<bucket>"
PATH_Data = PATH + "/Test"
PATH_Result = PATH + "/Results"
```

S3 permet aux différents noeuds du cluster EMR de lire les mêmes données et d'écrire les résultats dans un emplacement partagé.

## Rôle d'EMR

AWS EMR fournit un cluster Spark managé.

Son rôle est d'exécuter le traitement PySpark sur plusieurs machines, avec un driver et des workers. Cette configuration permet de passer d'une exécution locale limitée à une exécution distribuée sur l'ensemble des images.

Dans ce projet, EMR est utilisé comme environnement d'exécution pour :

- charger les images depuis S3 ;
- appliquer le preprocessing et l'extraction de features ;
- paralléliser les calculs avec Spark ;
- écrire les résultats en Parquet dans S3.

## Rôle du script bootstrap

Le fichier `bootstrap-emr.sh` installe les dépendances Python nécessaires lors de l'initialisation du cluster EMR.

Il installe notamment :

- `numpy` pour les calculs numériques ;
- `pillow` pour manipuler les images ;
- `pandas` pour les traitements tabulaires ;
- `pyarrow` pour le format Parquet ;
- `boto3`, `s3fs` et `fsspec` pour l'accès aux ressources S3.
- `tensorflow-cpu` pour exécuter MobileNetV2 sur un cluster CPU.

Cette étape évite d'installer manuellement les dépendances sur chaque noeud après le démarrage du cluster.

## Accès JupyterHub et tunnel SSH

Le notebook peut être exécuté depuis JupyterHub sur le cluster EMR.

Selon la configuration réseau du cluster, l'accès aux interfaces EMR, JupyterHub ou Spark History Server peut nécessiter :

- une clé SSH associée au cluster ;
- une règle de sécurité autorisant l'accès entrant depuis l'IP de travail ;
- un tunnel SSH vers le noeud master ;
- un proxy navigateur, par exemple FoxyProxy, pour accéder aux interfaces web internes.

Les captures du dossier `img/` documentent les étapes de configuration et d'accès utilisées pendant le projet.

## Résiliation du cluster

Un cluster EMR est facturé tant qu'il reste actif, même lorsque les notebooks ne tournent plus.

Après l'écriture des résultats dans S3 et la validation du traitement, il faut résilier le cluster depuis la console AWS ou via AWS CLI.

Cette étape est importante pour éviter des coûts cloud inutiles.
