import re
from typing import Dict, Match, Pattern

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
    _solved_strings: Dict[str, str] = {}

    def __init__(self) -> None:
        """Constructeur."""
        self.__resolvers: Dict[str, AbstractResolver] = {}

    def add_resolver(self, resolver: AbstractResolver) -> None:
        """Ajout un résolveur à la liste."""
        self.__resolvers[resolver.name] = resolver

    def resolve(self, string_to_solve_global: str) -> str:
        """Résout la chaîne à traiter et retourne la chaîne obtenue.
        Résout TOUT le paramétrage trouvé.

        Args:
            string_to_solve_global (str): chaîne globale à résoudre

        Raises:
            ResolverNotFoundError: levée si un résolveur demandé n'est pas trouvé

        Returns:
            str: chaîne résolue
        """
        return GlobalResolver._regex.sub(GlobalResolver.resolve_group, string_to_solve_global)

    @property
    def resolvers(self) -> Dict[str, AbstractResolver]:
        return self.__resolvers

    @staticmethod
    def resolve_group(match: Match[str]) -> str:
        """Résout la chaîne trouvé par la regex et permet de la remplacer.

        Args:
            match (Match[str]): groupe capturé par la regex

        Raises:
            ResolverNotFoundError: levée si le résolveur demandé n'est pas trouvé

        Returns:
            str: chaîne de remplacement
        """
        d_resolution = match.groupdict()
        # La chaîne complète, à remplacer, est donnée par la clé "param"
        s_all: str = d_resolution["param"]
        # Si cette chaîne n'est pas déjà dans _solved_strings
        if not s_all in GlobalResolver._solved_strings:
            # Le nom du résolveur est donnée par la clé "resolver_name"
            s_resolver_name: str = d_resolution["resolver_name"]
            # La chaîne à résoudre est donnée par la clé "to_solve"
            s_to_solve: str = d_resolution["to_solve"]
            # Vérification de l’existante du resolver
            if not s_resolver_name in GlobalResolver().resolvers:
                Config().om.debug(f"Resolvers : {', '.join(GlobalResolver().resolvers.keys())}")
                raise ResolverNotFoundError(s_resolver_name)
            # On résout globalement la chaîne à résoudre (si jamais on a des paramètres dans des paramètres...)
            s_to_solve = GlobalResolver().resolve(s_to_solve)
            # Puis on la résout avec le résolveur à utiliser et on l'ajoute à la liste
            s_solved = GlobalResolver().resolvers[s_resolver_name].resolve(s_to_solve)
            GlobalResolver._solved_strings[s_all] = s_solved
            Config().om.debug(f"resolve_group - {s_all} ({s_resolver_name} : {s_to_solve} => {s_solved})")
        Config().om.debug(f"resolve_group - {s_all} (from cache)")
        return GlobalResolver._solved_strings[s_all]
