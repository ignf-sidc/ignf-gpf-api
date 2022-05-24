import re
from typing import Dict, Pattern

from ignf_gpf_api.pattern.Singleton import Singleton
from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolverNotFoundError
from ignf_gpf_api.io.Config import Config


class GlobalResolver(metaclass=Singleton):
    """Classe permettant de résoudre une action en appelant les bons résolveurs.

    Attributes :
        __resolvers (Dict[str, AbstractResolver]): association nom du résolveur / résolveur.
    """

    _regex: Pattern[str] = re.compile(Config().get("workflow_resolution_regex", "global_regex"))

    def __init__(self) -> None:
        """Constructeur."""
        self.__resolvers: Dict[str, AbstractResolver] = {}

    def add_resolver(self, resolver: AbstractResolver) -> None:
        """Ajout un résolveur à la liste."""
        self.__resolvers[resolver.name] = resolver

    def resolve(self, s_to_solve_global: str) -> str:
        """Résout la chaîne à traiter et retourne la chaîne obtenue.
        Résout TOUT le paramétrage trouvé.

        Returns:
            str: chaîne obtenue
        """
        # Pour stocker les remplacements à effectuer
        d_old_new: Dict[str, str] = {}
        # On cherche les résolutions à effectuer
        l_resolutions = [result.groupdict() for result in GlobalResolver._regex.finditer(s_to_solve_global)]

        # On va résoudre les résolutions
        for d_resolution in l_resolutions:
            # La chaîne complète, à remplacer, est donnée par la clé "param"
            s_old: str = d_resolution["param"]
            # Si cette chaîne n'est pas déjà dans d_old_new
            if not s_old in d_old_new:
                # Le nom du résolveur est donnée par la clé "resolver_name"
                s_resolver_name: str = d_resolution["resolver_name"]
                # La chaîne à résoudre est donnée par la clé "to_solve"
                s_to_solve: str = d_resolution["to_solve"]
                # Vérification de l’existante du resolver
                if not s_resolver_name in self.__resolvers:
                    Config().om.debug(f"Resolvers : {', '.join(self.__resolvers.keys())}")
                    raise ResolverNotFoundError(s_resolver_name)
                # Résolution
                s_new = self.__resolvers[s_resolver_name].resolve(s_to_solve)
                # On ajoute à la liste
                d_old_new[s_old] = s_new

        # On a tout résolu, maintenant il faut remplacer
        s_solved = s_to_solve_global
        for s_old, s_new in d_old_new.items():
            s_solved = s_solved.replace(s_old, s_new)
        # Retour
        return s_solved
