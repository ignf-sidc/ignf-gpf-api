# Création d'une image docker pour héberger la documentation

## Création d'un fichier d'environnement

Récupérez le cod du dépôt :

```sh
git clone https://github.com/ignf-sidc/ignf-gpf-api.git
```

Créez dans ce dossier un fichier `.env` contenant :
* le tag/commit/branche dont vous souhaitez voir la doc ;
* le nom de projet docker compose (prefix du nom de l'image) ;
* le port d'exposition du conteneur ;
* le prefix pour nommer le conteneur.

```sh
cd ignf-gpf-api/docker
vim .env
```

Voici un exemple de fichier `.env` :

```sh
# Construction
TAG=dev
COMPOSE_PROJECT_NAME=doc__ignf_gpf_api

# Lancement de l'image
PORT=80
PREFIX=documentation
```

## Lancement de docker-compose

Lancez docker-compose, il va créer l'image et lancer le conteneur :

```sh
docker-compose up --build -d
```
