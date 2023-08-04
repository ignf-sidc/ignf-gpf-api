# Tutoriel 3 : publier un flux raster

La Géoplateforme permet d'héberger des flux raster pour permettre à vos utilisateur de les télécharger/utiliser.

Pour cela, vous devez téléverser des données « raster » sur lesquelles la Géoplateforme va effectuer des traitements.

Pour commencer, nous vous conseillons de suivre ce tutoriel qui vous permet de manipuler des données déjà existantes. Vous pouvez ensuite adapter chaque étape pour livrer vos données.

## Définition de la configuration

Suivez la page [configuration](configuration.md) pour définir le fichier de configuration.

## Récupération du jeu de données

Le jeu de données « 1_dataset_raster » contient des données raster à téléverser.

Récupérez les données en lançant la commande :

```sh
python -m ignf_gpf_api dataset -n 4_dataset_raster_gpf
```

Observez la structure du fichier :

```text
4_dataset_raster_gpf/
├── test
│   ├── 977-2018-0510-1979-U20N-0M50-E100.jp2
│   ├── 977-2018-0510-1979-U20N-0M50-E100.tab
│   ├── 977-2018-0510-1980-U20N-0M50-E100.jp2
│   ├── 977-2018-0510-1980-U20N-0M50-E100.tab
│   ├── 977-2018-0510-1981-U20N-0M50-E100.jp2
│   ├── 977-2018-0510-1981-U20N-0M50-E100.tab
│   ├── 977-2018-0510-1982-U20N-0M50-E100.jp2
│   └── 977-2018-0510-1982-U20N-0M50-E100.tab
├── test.md5
└── upload_descriptor.jsonc
```

Les données que la Géoplateforme va traiter sont situées dans le dossier `test`.
Le fichier `test.md5` permettra de valider les données téléversées côté Géoplateforme.

Enfin, le fichier `upload_descriptor.json` permet de décrire la livraison à effectuer.

## Fichier descripteur de livraison

Ouvrez le fichier `upload_descriptor.json` pour avoir plus de détails.

Il est composé d'une liste de `datasets` représentant chacun une livraison distincte.

Chaque dataset contient :

* la liste des dossiers à téléverser ;
* les informations de la livraison à créer (nom, description, srs et type) ;
* les commentaires et les tags à ajouter à la livraison. (Memo : les commentaires ne sont pas encore supporter par la version actuel de la gpf)

## Livraison des données

Livrez les données en indiquant le chemin du fichier descripteur au programme :

```sh
python -m ignf_gpf_api upload -f 4_dataset_raster_gpf/upload_descriptor.jsonc
```

Le programme doit vous indiquer que le transfert est en cours, puis qu'il attend la fin des vérification côté API avant de conclure que tout est bon. (Memo : cette partie est assez longue du à des problèmes de performance côté back. Le problème a déjà été remonté.)

## Workflow

Une fois les données livrées, il faut traiter les données avant de les publier (c'est à dire effectuer un (ou plusieurs) géo-traitement(s), puis configurer un géo-service et le rendre accessible).

Ces étapes sont décrites grâces à un workflow.

Vous pouvez récupérer un workflow d'exemple grâce à la commande suivante :

```sh
python -m ignf_gpf_api workflow -n generic_raster.jsonc
```

Ouvrez le fichier. Vous trouverez plus de détails dans la [documentation sur les workflows](workflow.md), mais vous pouvez dès à présent voir que le workflow est composé de 4 étapes. Il faudra lancer une commande pour chacune d'elles.

```mermaid
---
title: Workflow de publication de données Raster en WMS et WMST
---
%% doc mermaid ici https://mermaid-js.github.io/mermaid/#/flowchart?id=flowcharts-basic-syntax
flowchart TD
    A("upload") -->|pyramide| B("pyramide raster")
    B -->|configuration-WMST| C("configuration WMST")
    C -->|publication-WMST| D("offre WMST")
    B -->|configuration-WMS| E("configuration WMS")
    E -->|publication-WMS| F("offre WMS")
```

## Traitement et publication

Le workflow « generic_raster » permet de passer de la livraison à un flux WMS servant la donnée. Il comporte les étapes suivantes:

* `pyramide` : création d'une pyramide avec les données téléversées
* `configuration-WMST` : configuration d'un service de flux WMST à partir de la pyramide ;
* `publication-WMST` : publication du service de flux WMST sur le bon endpoint.
* `configuration-WMS` : configuration d'un service de flux WMS à partir de la pyramide ;
* `publication-WMS` : publication du service de flux WMS sur le bon endpoint.

La partie WMST et WMS sont indépendantes : elles peuvent être traitées en parallèle ou dans n'importe quel sens.

Les commandes à lancer sont les suivantes :

```sh
# partie création de la pyramide
python -m ignf_gpf_api workflow -f generic_raster.jsonc -s pyramide
# partie publication WMST
python -m ignf_gpf_api workflow -f generic_raster.jsonc -s configuration-WMST
python -m ignf_gpf_api workflow -f generic_raster.jsonc -s publication-WMST
# partie publication WMS
python -m ignf_gpf_api workflow -f generic_raster.jsonc -s configuration-WMS
python -m ignf_gpf_api workflow -f generic_raster.jsonc -s publication-WMS
```

La première commande ne doit pas être instantanée : un traitement est effectué et les logs doivent vous être remontés.

Le deux traitements suivants sont instantanés. A la fin, vous devez voir s'afficher un lien.
