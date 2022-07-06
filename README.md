# ignf-gpf-api

## Utilisation

### Comme exécutable

Créez un fichier `config.ini` avec :

```ini
[store_authentification]
# L'url de récupération du token d'authentification (cf. doc)
token_url=https://qlf-iam-gpf.ign.fr/auth/realms/master/protocol/openid-connect/token
# Votre login
login=LOGIN
# Votre mot de passe
password=PASSWORD
# Votre id client
client_id=geotuileur

[store_api]
# L'url d'entrée de l'API (cf. doc)
root_url=https://plage-geotuileur.ccs-ign-plage.ccs.cegedim.cloud/api/v1
# L'identifiant de votre entrepôt
datastore=DATASTORE_ID_TO_MODIFY
```

Vérifiez que l'identification est fonctionnelle :

```sh
# config.ini est directement trouvé s'il set dans le dossier de travail
python -m ignf_gpf_api auth
# Sinon indiquez le chemin
python -m ignf_gpf_api --ini /autre/chemin/config.ini auth
```

Cela devrait renvoyer :

```
Authentification réussie.
```

Affichez la configuration :

```sh
# Toute la configuration
python -m ignf_gpf_api config
# Une section
python -m ignf_gpf_api config -s store_authentification
# Une option d'une section
python -m ignf_gpf_api config -s store_authentification -o password
```

Envoyer des données :

```
python -m ignf_gpf_api upload -f tests/_data/test_datasets/1_test_dataset_vector/upload_descriptor.json
```

### Comme librairie

## Développement

### Mise en place de l'environnement de développement

Si nécessaire, installation système

```sh
sudo apt install python3 python3-pip python3-venv
```

Mise à jour de pip et virtualenv

```sh
python3 -m pip install --user --upgrade pip virtualenv setuptools
```

Création d'un environnement isolé

```sh
python3 -m venv env
```

Activation de l'environnement

```sh
source env/bin/activate
```

Installation basique

```sh
python3 -m pip install --upgrade pip setuptools flit
```

Installation de toutes les dépendances

```sh
python3 -m flit install --extras test
```

### Vérifications qualité

```sh
./check.sh
```

### Publication sur PyPI

```sh
export FLIT_PASSWORD=<token>
```

Publication sur TestPyPI :

```
flit publish --pypirc .pypirc --repository testpypi
```

Publication sur PyPI :

```
flit publish --pypirc .pypirc --repository pypi
```
