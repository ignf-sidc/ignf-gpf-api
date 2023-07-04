# Configuration

Ce module Python vient avec une configuration par défaut vous permettant de définir un minimum de paramètres.
Vous pouvez cependant écraser chaque paramètre par défaut en redéfinissant sa valeur dans un nouveau fichier de configuration.

Certains paramètres (comme vos identifiants d'API) **doivent** être redéfinis.

La configuration est composée de sections elles-même composées d'options.

Voici un exemple reprenant la structure d'un fichier de configuration :

```ini
[section_1]
option_1=valeur_1_1
option_2=valeur_1_2

[section_2]
option_1=valeur_2_1
option_2=valeur_2_2
option_3=valeur_2_3
```

Nous pouvons faire référence à la `valeur_1_1` par l'intitulé `section_1.option_1`.

## Votre fichier de configuration

Créez un fichier `config.ini` à la racine du projet.

Il faudra à minima renseigner vos identifiants API (section `store_authentification`) et l'entrepôt (*datastore*) sur lequel vous allez travailler (section `store_api`).

Voici un exemple de ce que cela peut donner :

```ini
[store_authentification]
# L'url de récupération du token d'authentification (cf. doc)
token_url=https://qlf-iam-gpf.ign.fr/auth/realms/master/protocol/openid-connect/token
# Groupe d’appartenance
client_id=geotuileur
# Votre login
login=LOGIN
# Votre mot de passe
password=PASSWORD

[store_api]
# L'url d'entrée de l'API (cf. doc)
root_url=https://plage-geotuileur.ccs-ign-plage.ccs.cegedim.cloud/api/v1
# L'identifiant de votre entrepôt
datastore=DATASTORE_ID_TO_MODIFY
```

Explication sur les paramètres :

* `store_authentification` : paramètres concernant l'authentification sur la Géoplateforme :
    * `token_url` : URL pour récupérer le jeton d'authentification (consulter la doc de l'API si nécessaire) ;
    * `client_id` : votre groupe d’appartenance ;
    * `login` : votre nom d'utilisateur ;
    * `password` : votre mot de passe ;
* `store_api` : paramètres concernant votre Entrepôt sur la Géoplateforme :
    * `root_url` : URL racine de l'API (consulter la doc de l'API si nécessaire) ;
    * `datastore` : l'identifiant du datastore à gérer (voir ci-dessous).

Dans la configuration, vous devez indiquer l'identifiant du datastore à utiliser. Celui est lié à la communauté à laquelle vous appartenez.

Si vous ne savez pas quoi mettre, il est possible de lister les communautés auxquelles vous participez et, pour chacune d'elle, le datastore qui lui est associé. Cela vous permet de récupérer cet identifiant.

La commande pour lister les communautés auxquelles vous appartenez est la suivante :

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

## Utilisation via l'exécutable

Ce module Python est utilisable comme exécutable. Dans ce cas vous avez deux manières d'indiquer au programme votre fichier de configuration :

* vous pouvez nommez le fichier `config.ini` et le mettre dans le répertoire courant ;
* vous pouvez indiquer au programme le chemin vers votre fichier via le paramètre `--ini` :
```sh
python -m ignf_gpf_api --ini chemin/vers/config.ini
```

## Utilisation via un script

Si vous utilisez ce module Python dans un script, il faudra ouvrir le fichier de configuration via la classe [Config][ignf_gpf_api.io.Config.Config] au début de celui-ci :

```python
# Importez la classe Config
from ignf_gpf_api.io.Config import Config

# Ajoutez votre fichier de configuration (adaptez le chemin)
Config().read("config.ini")

# Suite de votre script...
```
