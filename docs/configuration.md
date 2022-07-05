# Configuration

Le module Python vient avec une configuration par défaut vous permettant de ne pas avoir à définir grand chose.

Vous pouvez cependant écraser chaque paramètre par défaut en reprisant sa valeur dans un nouveau fichier de configuration.

Certains paramètres (comme vos identifiants d'API) doivent être redéfinis.

## Votre fichier de configuration

Créez un fichier `config.ini` avec au minimum :

```ini
[store_authentification]
# L'url de récupération du token d'authentification (cf. doc)
token_url=https://qlf-iam-gpf.ign.fr/auth/realms/master/protocol/openid-connect/token
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
    * `login` : votre nom d'utilisateur ;
    * `password` : votre mot de passe ;
* `store_api` : paramètres concernant votre Entrepôt sur la Géoplateforme :
    * `root_url` : URL racine de l'API (consulter la doc de l'API si nécessaire) ;
    * `datastore` : l'identifiant du datastore à gérer.

## Utilisation via l'exécutable

Ce module Python est utilisable comme exécutable. Dans ce cas vous avez deux manières d'indiquer au programme votre fichier de configuration :

* vous pouvez nommez le fichier `config.ini` et le mettre dans le répertoire courant ;
* vous pouvez indiquer au programme le chemin vers votre fichier via le paramètre `--ini` :
```sh
python -m ignf_gpf_api --ini chemin/vers/config.ini
```

## Utilisation via un script

Si vous utilisez ce module Python dans un script, il faudra ouvrir le fichier de configuration via la classe `Config` au début de celui-ci :

```python
# Importez la classe Config
from ignf_gpf_api.io.Config import Config

# Ajoutez votre fichier de configuration (adaptez le chemin)
Config().read("config.ini")

# Suite de votre script...
```
