# Utilisation comme exécutable

## Configuration

Pensez à [créer un fichier de configuration](configuration.md) indiquant au minimum vos identifiants.

## Vérification de la configuration

Un bon moyen de vérifier que la configuration est correcte est de s'authentifier via l'exécutable :

```sh
# Le fichier de configuration est directement trouvé s'il est
# nommé "config.ini" et qu'il est situé dans le dossier de travail
python -m ignf_gpf_api auth
# Sinon indiquez son chemin
python -m ignf_gpf_api --ini /autre/chemin/config.ini auth
```

Cela devrait renvoyer :

```txt
Authentification réussie.
```

## Afficher toute la configuration

Vous pouvez afficher toute la configuration via une commande. Cela peut vous permettre d'avoir une liste exhaustive des paramètres disponibles et de vérifier que votre fichier de configuration a bien le dernier mot sur les paramètres à utiliser.

Affichez la configuration :

```sh
# Toute la configuration
python -m ignf_gpf_api config
# Une section
python -m ignf_gpf_api config -s store_authentification
# Une option d'une section
python -m ignf_gpf_api config -s store_authentification -o password
```

## Récupérer des jeux de données d'exemple

Il est possible de récupérer des jeux de données d'exemple via l'exécutable.

Lancez la commande suivante pour lister les jeux disponibles :

```sh
python -m ignf_gpf_api dataset
```

Lancez la commande suivante pour extraire un jeu de donnée :

```sh
python -m ignf_gpf_api dataset -n 1_dataset_vector
```

Les données seront extraites dans le dossier courant, vous pouvez préciser la destination avec le paramètre `--folder` (ou `-f`).


## Envoyer des données

Pour envoyer des données, vous devez générer un [fichier descripteur de livraison](upload_descriptor.md).

C'est un fichier au format JSON permettant de décrire les données à livrer et les livraisons à créer.

Ensuite, vous pouvez simplement livrer des données :

```sh
python -m ignf_gpf_api upload -f mon_fichier_descripteur.json
```

Les jeux de données d'exemple sont fournis avec le fichier descripteur (voir [Récupérer des jeux de données d'exemple](#recuperer-des-jeux-de-donnees-dexemple)).


## Réaliser des traitements et publier des données

Pour réaliser des traitements et publier des données géographiques, vous devez générer un [fichier workflow](workflow.md).

C'est un fichier au format JSON permettant de décrire, en une suite d'étapes, les traitements et les publications à effectuer.

Vous pouvez valider votre workflow :

```sh
python -m ignf_gpf_api workflow -f mon_workflow.json
```

Ensuite, vous pouvez simplement lancer une étape :

```sh
python -m ignf_gpf_api workflow -f mon_workflow.json -s mon_étape
```
