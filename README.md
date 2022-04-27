# ignf-gpf-api

## Développement

### Mise en place de l'environnement de développement

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

Installation basiques

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
