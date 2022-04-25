# ignf-gpf-api

## Développement

### Lancement de pylint

```sh
pylint --rcfile=.pylintrc ignf_gpf_api --recursive=y
```


### Lancement de black

```sh
black
```


### Lancement de pylint

```sh
mypy ignf_gpf_api
```

### Publication sur PyPI

Publication sur TestPyPI :

```
flit --repository testpypi publish
```

Publication sur PyPI :

```
flit --repository pypi publish
```
