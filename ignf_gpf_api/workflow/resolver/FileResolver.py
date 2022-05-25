from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolverError


class FileResolver(AbstractResolver):
    """Classe permettant de résoudre des paramètres fichiers.
    Exemple de fichiers :
        titi.txt => "coucou"
        list.json => ["coucou1", "coucou2"]
        dict.json => {"k1":"v1", "k2":"v2"}

    Quoi faire :
        str => lire le fichier et point barre
        list => vérifier que c'est une liste et renvoi la liste en JSON str
        dict => vérifier que c'est un dict et renvoi la liste en JSON str

    Exemples :
        "{file.str(titi.txt)}" => "coucou"
        ["{file.list(list.json)}"] => '["coucou1", "coucou2"]'
        {"{file.dict(dict.json)}":"value"} => '{"k1":"v1", "k2":"v2"}'

    Attributes :
        __name (str): nom de code du resolver
    """

    def resolve(self, s_to_solve: str) -> str:
        raise ResolverError(self.name, s_to_solve)
