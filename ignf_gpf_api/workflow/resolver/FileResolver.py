import re
import json
from pathlib import Path

from ignf_gpf_api.workflow.action.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.action.Errors import ResolveFileError, UnknowFileError, ResolverError
from ignf_gpf_api.io.Config import Config
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

    _file_regex = re.compile(Config().get("workflow_resolution_regex", "file_regex"))

    def __resolve_str(self, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier texte
           on valide que le contenu est bien un texte
        Args:
            s_path (str): string du path du fichier à ouvrir

        Returns:
            str: texte contenu dans le fichier
        """
        p_path_text = Path(s_path)
        if p_path_text.exists():
            s_result = str(p_path_text.read_text(encoding="UTF-8").rstrip("\n"))
            # si la string est vide
            if not s_result:
                raise ResolveFileError("fichier_string", f"le fichier {s_path} est vide")
        else:
            raise ResolveFileError("fichier_string", f"le fichier {p_path_text} n'existe pas")
        return s_result

    def __resolve_list(self, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier contenant une liste
           on valide que le contenu est bien une liste

        Args:
            s_path (str): string du path du fichier à ouvrir
        Returns:
            str: liste contenu dans le fichier
        """
        s_data = self.__resolve_str(s_path)
        # on vérifie que cela est bien une liste
        if not isinstance(json.loads(s_data), list):
            raise ResolverError("fichier_list", f"le fichier {s_path} ne contient pas une liste")

        return s_data

    def __resolve_dict(self, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier contenant un dictionnaire
           on valide que le contenu est bien un dictionnaire

        Args:
            s_path (str): string du path du fichier à ouvrir

        Returns:
            str: dictionnaire contenu dans le fichier
        """
        s_data = self.__resolve_str(s_path)
        # on vérifie que cela est bien un dictionnaire
        if not isinstance(json.loads(s_data), dict):
            # le programme emet une erreur
            raise ResolverError("fichier_dict", f"le fichier {s_path} ne contient pas un dictionnaire")
        return s_data

    def resolve(self, s_to_solve: str) -> str:
        """Fonction permettant de renvoyer sous forme de string la resolution
        des paramètres de fichier passées en entrée.

        Args:
            s_to_solve (str): string dont on extrait l'information du type de l'information contenu dans
            le document et le path du fichier

        Raises:
            ResolverError: si le type n'est pas reconnu

        Returns:
            str: le contenu du fichier en entrée sous forme de string
        """
        s_result = ""
        # On cherche les résolutions à effectuer
        o_result = FileResolver._file_regex.search(s_to_solve)
        if o_result is None:
            raise ResolveFileError(self.name, s_to_solve)
        d_groups = o_result.groupdict()
        if d_groups["resolver_type"] == "str":
            s_result = str(self.__resolve_str(d_groups["resolver_file"]))
        elif d_groups["resolver_type"] == "list":
            s_result = str(self.__resolve_list(d_groups["resolver_file"]))
        elif d_groups["resolver_type"] == "dict":
            s_result = str(self.__resolve_dict(d_groups["resolver_file"]))
        else:
            raise UnknowFileError(s_to_solve, "type inconnu")
        return s_result
