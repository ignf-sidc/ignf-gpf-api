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

``` txt
Authentification réussie.
```

## Mes datastores

Dans la configuration, vous devez indiquer l'identifiant du datastore à utiliser.

Si vous ne le connaissez pas, il est possible de lister les communautés auxquelles vous participez et, pour chacune d'elle, le datastore qui lui est associé.

Commande pour lister les communautés auxquelles vous appartenez :

```sh
python -m ignf_gpf_api me
```

Cela devrait renvoyer :

```
Vos informations :
  * email : prenom.nom@me.io
  * nom : Prénom Nom
  * votre id : 100000000000000000000024

Vous êtes membre de 1 communauté(s) :

  * communauté « Bac à sable » :
      - id de la communauté : 200000000000000000000024
      - id du datastore : 300000000000000000000024
      - nom technique : bac-a-sable
      - droits : community, uploads, processings, datastore, stored_data, broadcast
```

Dans cet exemple, l'identifiant du datastore à utiliser est `300000000000000000000024`.

!!! warning "Attention"

    Cela ne fonctionnera que si les autres paramètres (nom d'utilisateur, mot de passe et urls) sont corrects.


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


## Tutoriels

Vous pouvez maintenant livrer et publier vos données en utilisant le module comme un exécutable. Voici quelques exemples :

* [Tutoriel 1 : héberger une archive pour la rendre téléchargeable](tutoriel_1_archive.md)
* [Tutoriel 2 : téléverser des données vecteur les publier en flux](tutoriel_2_flux_vecteur.md)
