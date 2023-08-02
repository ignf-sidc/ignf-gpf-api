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

## Documentation

Vous pouvez générer la doc en local via la commande :

```sh
mkdocs serve
```

## Développement et tests

Pour tester le programme, vous aurez besoin de créer un fichier `config.ini`, cf. [configuration](configuration.md).

Les classes python sont couvertes avec un maximum de tests unitaires merci de penser à couvrir le code ajouté ou à modifier les tests existants au besoin.

Pensez à activer l'environnement avant de lancer les tests :

```sh
source env/bin/activate
```

Pour automatiser dans VSCode : [doc ici](https://code.visualstudio.com/docs/python/environments#_work-with-python-interpreters)

À la fin de votre développement, lancez `./check.sh` pour vérifier que votre code respecte les critères de qualité.

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

## Déploiement des versions dev et prod sur PyPI

### Mise à jour des branches prod et dev

Pour effectuer un déploiment de la librairie ignf-gpf-api, il faut d'abord modifier le numéro de version dans le fichier `__init__.py` dans le dossier ignf_gpf_api/ignf_gpf_api/ .

```py
__version__ = <x.y.z>
```
Par exemple, on a "0.1.9". On va donc écrire "0.1.10".
Commiter en précisant le numéro de version dans le message de commit.

Puis il faut résoudre ou faire les pull request avec la branche dev en fonction de l'avancement du projet pour avoir une branche dev à jour.
Idem avec la branche prod si besoin.

### Création de la (pre)-release

Pour publier une nouvelle version, qui va être ensuite publiée comme librairie sur PyPi, il faut [créer une (pre)-release](https://github.com/ignf-sidc/ignf-gpf-api/releases/new) :

- créez une release de test sur la branche **dev** versionnée selon le modèle `tx.y.z` (ex : t1.2.3) pour déployer une nouvelle version du module en test : 
  - choose a tag : taper "t0.1.10" et cliquer sur "Create new tag".
  - target : choisir "dev"
  - ajouter un titre ("Test 1.2.3"), et une description des principales modifications apportées. 
  - Cocher la case pre-release. Cliquer sur "Publish release" (les tests vont se lancer...)
  - Vérifier la publication sur [test.pypi](https://test.pypi.org/project/ignf_gpf_api/)

- créez une release sur la branche **prod** versionnée selon le modèle `vx.y.z` (ex : v1.2.3) pour déployer une nouvelle version du module en production : 
  - choose a tag : taper "v0.1.10" et cliquer sur "Create new tag".
  - target : choisir "prod"
  - ajouter un titre ("Version 1.2.3"), et une description des principales modifications apportées. 
  - Cliquer sur "Publish release" (les tests vont se lancer...)
  - Vérifier la publication sur [pypi](https://pypi.org/project/ignf_gpf_api/)

### Publication sur PyPI

La publication du package sur PyPI est automatique sur Github grâce aux actions [CI Dev](https://github.com/ignf-sidc/ignf-gpf-api/actions/workflows/ci-dev.yml) et [CI Prod](https://github.com/ignf-sidc/ignf-gpf-api/actions/workflows/ci-prod.yml) :


Si besoin, voici les commandes pour effectuer à la main la publication :
 
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
