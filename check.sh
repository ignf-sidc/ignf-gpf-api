# Lancement des tests
python3 -m unittest discover -b -p *TestCase.py

# Lancement de pylint
pylint --rcfile=.pylintrc ignf_gpf_api --recursive=y
pylint --rcfile=.pylintrc tests --recursive=y

# Lancement de black
black ignf_gpf_api tests

# Lancement de pylint
mypy --strict ignf_gpf_api tests
