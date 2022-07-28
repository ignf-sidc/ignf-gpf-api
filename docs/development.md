# Développement

## Mise en place

Récupérez le code :

```sh
git clone git@github.com:ignf-sidc/ignf-gpf-api.git
```

Ouvrez le dossier nouvellement crée avec votre éditeur favoris (ici [Visual Studio Code](https://code.visualstudio.com/)) :

```sh
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

Créez un environnement isolé : (il sera créé dans le dossier où la commande est lancée donc il est préférable de se placer dans le dossier `ignf-gpf-api`)

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

## Développement et tests

Pour tester le programme, vous aurez besoin de créer un fichier `config.ini`, cf. [configuration](configuration.md).

Les classes python sont couvertes avec un maximum de tests unitaires donc avec le développement/modification d'une classe/fonction il faut développer/modifier les tests unitaires de l'élément.

Pensez à activer l'environnement avant de lancer les tests :

```sh
source env/bin/activate
```

Pour automatiser dans VSCode : [doc ici](https://code.visualstudio.com/docs/python/environments#_work-with-python-interpreters)

À la fin de votre développement, lancez `check.sh` pour vérifier que votre code respecte les critères de qualité du code.

### Consigne développement

- Nomenclature Python (classes en PascalCase, constantes en UPPER_CASE, le reste en snake_case)​
- Variables suffixées par leur type (cf. "variable-rgx" du .pylintrc)​
  - `s_` : string​
  - `i_` : integer​
  - `f_` : float​
  - `l_` : list (et autres enumerable)​
  - `d_` : dict​
  - `b_` : bool​
  - `e_` : error​
  - `p_` : Path​
  - `o_` : object​
- Programmation typée (vérifiée avec mypy; [memo type](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html))
- Toutes les classes et fonctions doivent être documentées.
- Utilisation de pathlib.Path et non de os.path​
- Gérer l'affichage des messages avec `Config().om​`, ne pas utiliser de `print()` ou autre logger.
  - Config().om.debug("message")
  - Config().om.info("message")
  - Config().om.warning("message")
  - Config().om.error("message")
  - Config().om.critical("message")
- Configuration centralisée via la classe Config()​ (cf. [Utilisation comme module Python](comme-module.md))

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

```sh
flit publish --pypirc .pypirc --repository testpypi
```

Publication sur PyPI :

```sh
flit publish --pypirc .pypirc --repository pypi
```
