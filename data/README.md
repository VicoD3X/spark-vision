# Données et artefacts

Ce dossier documente les données attendues par le projet. Le dataset complet n'est pas versionné dans Git afin de garder le dépôt léger et exploitable.

## Dataset attendu

Les images utilisées proviennent du dataset Fruits-360.

Pour lancer le notebook en local, placer les données sous l'arborescence suivante :

```text
data/fruits-360_dataset/fruits-360/Test/
```

Le notebook charge les fichiers `.jpg` de manière récursive et extrait le label depuis le nom du dossier parent de chaque image.

## Résultats générés

Les résultats Spark sont écrits dans :

```text
data/Results/
```

Ce dossier n'est pas versionné. Il peut contenir plusieurs fichiers Parquet générés par Spark, par exemple :

```text
part-00000-....snappy.parquet
_SUCCESS
```

## Exécution cloud

Dans la version AWS EMR, les données sont attendues sur Amazon S3.

Le notebook utilise le même principe :

- un dossier S3 d'entrée contenant les images ;
- un dossier S3 de sortie contenant les résultats Parquet ;
- un accès partagé entre le driver Spark et les workers du cluster EMR.

## Pourquoi ces fichiers ne sont pas inclus

Les images Fruits-360 et les résultats Parquet peuvent devenir volumineux. Les conserver hors Git évite d'alourdir le dépôt et garde le projet centré sur le code, la documentation et la démarche technique.
