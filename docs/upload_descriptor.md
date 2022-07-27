# Fichier descripteur de livraison

Creation d'un fichier json

Chaque dataset contient :

* la liste des dossiers à téléverser
    * Data_dirs -> chemin relatif

* les informations de la livraison à créer
    * Nom (choix libre)
    * Description (choix libre)
    * Srs -> EPSG:2154 | 2154 | Lam93
    * Type : Le type de la livraison conditionne les types de fichiers de données qui seront attendus et les traitements qui pourront prendre en entrée cette livraison. Rien n'interdit de déposer des données avec des extensions incohérentes avec le type de livraison, mais elles ne seront potentiellement pas prises en compte par les vérifications et les traitements.
        * RASTER -> PNG, TIFF, JPEG, JPEG2000
        * VECTOR -> SHP, CSV, GeoJSON
        * ARCHIVE -> Tout types de fichiers

* les commentaires et les tags à ajouter à la livraison.
    * Comments (choix libre et multiple)
    * Tags (choix libre et multiple)

exemple avec 1 dataset :
```
{
    "datasets": [
        {
            "data_dirs": [
                "CANTON"
            ],
            "upload_infos": {
                "description": "Jeu d'exemple vecteur",
                "name": "EXAMPLE_DATASET_VECTOR",
                "srs": "EPSG:2154",
                "type": "VECTOR"
            },
            "comments": [
                "Ceci est un jeu de données d'exemple contenant des données vecteur"
            ],
            "tags": {
                "tuto": "oui"
            }
        }
    ]
}
```

exemple avec plusieurs datasets :
```
{
    "datasets": [
        {
            "data_dirs": [
                "image_raster"
            ],
            "upload_infos": {
                "description": "Jeu d'exemple rasteur",
                "name": "EXAMPLE_DATASET_RASTER",
                "srs": "EPSG:2154",
                "type": "RASTER"
            },
            "comments": [
                "Ceci est un jeu de données d'exemple contenant des données raster"
            ],
            "tags": {
                "tuto": "oui"
            }
        },
        {
            "data_dirs": [
                "shapefile"
            ],
            "upload_infos": {
                "description": "Jeu d'exemple shp",
                "name": "EXAMPLE_DATASET_SHP",
                "srs": "EPSG:2154",
                "type": "VECTOR"
            },
            "comments": [
                "Ceci est un jeu de données d'exemple contenant des données vector"
            ],
            "tags": {
                "tuto": "oui"
            }
        },

    ]
}
```

[Envoyer les données](comme-executable.md#envoyer-des-donnees)
