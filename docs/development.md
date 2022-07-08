# Développement

## Mise en place

Récupérez le code :

```sh
git clone git@github.com:ignf-sidc/ignf-gpf-api.git
```

Ouvrez le dossier nouvellement crée avec votre éditeur favoris (ici [Visual Studio Code](https://code.visualstudio.com/)) :

```
code ignf-gpf-api
```

Si nécessaire, effectuez les installations systèmes suivantes :

```sh
sudo apt install python3 python3-pip python3-venv
```

Puis mettez à jour `pip` et `virtualenv` :

```sh
python3 -m pip install --user --upgrade pip virtualenv setuptools
```

Créez un environnement isolé :

```sh
python3 -m venv env
```

Activez l'environnement :

```sh
source env/bin/activate
```

Installez les dépendances de développement :

```sh
python3 -m pip install --upgrade pip setuptools flit
python3 -m flit install --extras all
```

Lancez les tests pour vérifier que tout fonctionne correctement :

```sh
./check.sh
```

## Développement

Pour tester le programme, vous aurez besoin de créer un fichier `config.ini`, cf. [configuration](configuration.md).

À la fin de votre développement, lancez `check.sh` pour vérifier que votre code respecte les critères de qualité du code.

## Documentation

Vous pouvez générer la doc en local via la commande :

```sh
mkdocs serve
```

## Publication sur PyPI

La publication du package sur PyPI est automatique sur Github après la [création d'une release](https://github.com/ignf-sidc/ignf-gpf-api/releases/new).

Si besoin, voici les commandes pour l'effectuer à la main :

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
