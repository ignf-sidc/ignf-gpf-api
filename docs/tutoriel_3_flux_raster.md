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
python -m ignf_gpf_api dataset -n 1_dataset_raster_gpf
```

Observez la structure du fichier :

```
1_dataset_raster_gpf/
├── test
│   //TODO: mettre les noms des fichiers
├── test.md5
└── upload_descriptor.json
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

Livrer les données en indiquant le chemin du fichier descripteur au programme :

```sh
python -m ignf_gpf_api upload -f 1_dataset_raster_gpf/upload_descriptor.json
```

Le programme doit vous indiquer que le transfert est en cours, puis qu'il attend la fin des vérification côté API avant de conclure que tout est bon. (Memo : cette partie est assez longue du à des problèmes de performance côté Wordline. Le problème a déjà été remonté.)

## Workflow

Une fois les données livrées, il faut traiter les données avant de les publier (c'est à dire effectuer un (ou plusieurs) géo-traitement(s),
puis configurer un géo-service et le rendre accessible).

Ces étapes sont décrites grâces à un workflow.

Vous pouvez récupérer un workflow d'exemple grâce à la commande suivante :

```sh
python -m ignf_gpf_api workflow -n wms-generic_gpf.jsonc
```

Ouvrez le fichier. Vous trouverez plus de détails dans la [documentation sur les workflows](workflow.md), mais vous pouvez dès à présent voir que le workflow est composé de 4 étapes. Il faudra lancer une commande pour chacune d'elles.
// TODO: compléter partie aprés creation du workflow WMS soit faire le diagramme

## Traitement et publication

Le workflow « wms-generic » permet de passer de la livraison à un flux WMS servant la donnée. Il comporte //TODO liste des étapes:

// TODO commandes 

La première commandes ne doit pas être instantanée : un traitement est effectué et les logs doivent vous être remontés.

Le deux traitements suivants sont instantanés. A la fin, vous devez voir s'afficher un lien.

Exemple :

//TODO faire l'exemple récupération lien données WMS
