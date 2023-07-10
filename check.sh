declare -i code=0

# Lancement de pylint
pylint --rcfile=.pylintrc --disable=fixme ignf_gpf_api --recursive=y
code+=$?
pylint --rcfile=.pylintrc --disable=fixme tests --recursive=y
code+=$?
echo

# Lancement de black
black ignf_gpf_api tests
code+=$?
echo

# Lancement de mypy
mypy --strict ignf_gpf_api tests
code+=$?
echo

# Lancement des tests et vérification de la couverture
coverage run -m unittest discover -b -p *TestCase.py
code+=$?
coverage report --fail-under=75
code+=$?
coverage html

# Affichage synthétique
if [ $code -eq 0 ]
then
    printf "\n\033[0;32mOK\033[0m\n";
else
    printf "\n\033[0;31mKO\033[0m\n";
fi

# Retour
exit $code
