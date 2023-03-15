import re
import json
from pathlib import Path

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolveFileInvalidError, ResolveFileNotFoundError, ResolverError


class FileResolver(AbstractResolver):
    """Classe permettant de résoudre des paramètres faisant référence à des fichiers.

    Ce résolveur permet d'insérer le contenu d'un fichier au moment de la résolution.

    Ce fichier peut être un fichier texte basique, une liste au format JSON ou un dictionnaire au format JSON.


    Fichier texte :

        Contenu du fichier `exemple.txt` :

        ```txt
        coucou
        ```

        Chaîne à remplacer : `Je veux dire : {file.str(exemple.txt)}`

        Résultat : `Je veux dire : coucou`


    Fichier de liste :

        Contenu du fichier `list.json` :

        ```json
        ["valeur 1", "valeur 2"]
        ```

        Chaîne à remplacer : `{"values": "{file.str(list.json)"]}`

        Résultat : `{"values": ["valeur 1", "valeur 2"]}`


    Fichier de clé-valeur :

        Contenu du fichier `dict.json` :

        ```json
        {"k1":"v1", "k2":"v2"}
        ```

        Chaîne à remplacer : `{"parameters": {"{file.dict(dict.json)}":"value"}}`

        Résultat : `{"parameters": {"k1":"v1", "k2":"v2"}}`

    Attributes:
        __name (str): nom de code du resolver
    """

    _file_regex = re.compile(Config().get("workflow_resolution_regex", "file_regex"))

    def __resolve_str(self, string_to_solve: str, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier texte
           on valide que le contenu est bien un texte
        Args:
            string_to_solve (str): chaîne à résoudre
            s_path (str): string du path du fichier à ouvrir

        Returns:
            texte contenu dans le fichier
        """
        p_path_text = Path(s_path)
        if p_path_text.exists():
            s_result = str(p_path_text.read_text(encoding="UTF-8").rstrip("\n"))
        else:
            raise ResolveFileNotFoundError(self.name, string_to_solve)
        return s_result

    def __resolve_list(self, string_to_solve: str, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier contenant une liste
           on valide que le contenu est bien une liste

        Args:
            string_to_solve (str): chaîne à résoudre
            s_path (str): string du path du fichier à ouvrir
        Returns:
            liste contenue dans le fichier
        """
        s_data = self.__resolve_str(string_to_solve, s_path)
        # on vérifie que cela est bien une liste
        try:
            l_to_solve = json.loads(s_data)
        except json.decoder.JSONDecodeError as e_not_list:
            raise ResolveFileInvalidError(self.name, string_to_solve) from e_not_list

        if not isinstance(l_to_solve, list):
            raise ResolveFileInvalidError(self.name, string_to_solve)

        return s_data

    def __resolve_dict(self, string_to_solve: str, s_path: str) -> str:
        """fonction privé qui se charge d'extraire une string d'un fichier contenant un dictionnaire
           on valide que le contenu est bien un dictionnaire

        Args:
            string_to_solve (str): chaîne à résoudre
            s_path (str): string du path du fichier à ouvrir

        Returns:
            dictionnaire contenu dans le fichier
        """
        s_data = self.__resolve_str(string_to_solve, s_path)
        # on vérifie que cela est bien un dictionnaire
        try:
            d_to_solve = json.loads(s_data)
        except json.decoder.JSONDecodeError as e_not_list:
            raise ResolveFileInvalidError(self.name, string_to_solve) from e_not_list

        if not isinstance(d_to_solve, dict):
            # le programme émet une erreur
            raise ResolveFileInvalidError(self.name, string_to_solve)
        return s_data

    def resolve(self, string_to_solve: str) -> str:
        """Fonction permettant de renvoyer sous forme de string la resolution
        des paramètres de fichier passés en entrée.

        Args:
            string_to_solve (str): chaîne à résoudre (type de fichier à traiter et chemin)

        Raises:
            ResolverError: si le type n'est pas reconnu

        Returns:
            le contenu du fichier en entrée sous forme de string
        """
        s_result = ""
        # On cherche les résolutions à effectuer
        o_result = FileResolver._file_regex.search(string_to_solve)
        if o_result is None:
            raise ResolverError(self.name, string_to_solve)
        d_groups = o_result.groupdict()
        if d_groups["resolver_type"] == "str":
            s_result = str(self.__resolve_str(string_to_solve, d_groups["resolver_file"]))
        elif d_groups["resolver_type"] == "list":
            s_result = str(self.__resolve_list(string_to_solve, d_groups["resolver_file"]))
        elif d_groups["resolver_type"] == "dict":
            s_result = str(self.__resolve_dict(string_to_solve, d_groups["resolver_file"]))
        else:
            raise ResolverError(self.name, string_to_solve)
        return s_result
