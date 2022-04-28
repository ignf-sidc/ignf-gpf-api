"""API Python pour simplifier l'utilisation de l'API Entrepôt Géoplateforme."""

import configparser
import io
import sys
import argparse
import traceback
from pathlib import Path
from typing import Optional, Sequence

import ignf_gpf_api
from ignf_gpf_api.Error import GpfApiError
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.auth.Authentifier import Authentifier


def main() -> None:
    """Fonction d'entrée."""
    # Résolution des paramètres utilisateurs
    cArgs = parse_args()

    # Résolution de la config
    if not Path(cArgs.config).exists():
        raise GpfApiError(f"Le fichier de configuration précisé ({cArgs.config}) n'existe pas.")
    Config().read(cArgs.config)

    # Exécution de l'action demandée
    if cArgs.task == "auth":
        auth(cArgs)
    elif cArgs.task == "config":
        config(cArgs)


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse les paramètres utilisateurs.

    Args:
        args (Optional[Sequence[str]], optional): paramètres à parser, si None sys.argv utilisé. Defaults to None.

    Returns:
        argparse.Namespace: paramètres
    """
    # Parsing des paramètres
    cParser = argparse.ArgumentParser(prog="ignf_gpf_api", description="Exécutable pour interagir avec l'API Entrepôt de la Géoplateforme.")
    cParser.add_argument("--ini", dest="config", default="config.ini", help="Chemin vers le fichier de config à utiliser (config.ini par défaut)")
    cParser.add_argument("--version", action="version", version=f"%(prog)s v{ignf_gpf_api.__version__}")
    cSubParsers = cParser.add_subparsers(dest="task", metavar="TASK", required=True, help="Tâche à effectuer")
    # Parser for auth
    cParserAuth = cSubParsers.add_parser("auth", help="Authentification")
    cParserAuth.add_argument("--show", type=str, choices=["token", "header"], default=None, help="Donnée à renvoyer")
    # Parser for config
    cParserAuth = cSubParsers.add_parser("config", help="Configuration")
    cParserAuth.add_argument("--file", "-f", type=str, default=None, help="Chemin du fichier où sauvegarder la configuration (si null, la configuration est affichée)")
    cParserAuth.add_argument("--section", "-s", type=str, default=None, help="Se limiter à une section")
    cParserAuth.add_argument("--option", "-o", type=str, default=None, help="Se limiter à une option (section doit être renseignée)")
    return cParser.parse_args(args)


def auth(cArgs: argparse.Namespace) -> None:
    """Authentifie l'utilisateur et retourne les informations de connexion demandées.
    Si aucune information est demandée, confirme juste la bonne authentification.

    Args:
        cArgs (argparse.Namespace): paramètres utilisateurs
    """
    sToken = Authentifier().get_access_token_string()
    if cArgs.show == "token":
        print(sToken)
    elif cArgs.show == "header":
        print(Authentifier().get_http_header())
    else:
        print("Authentification réussie.")


def config(cArgs: argparse.Namespace) -> None:
    """Fonction pour afficher ou sauvegarder la configuration :
    * si une section (voire une option) est demandée, on affiche ce qui est demandé
    * sinon :
        * si un fichier est précisé on y enregistre toute la config
        * sinon on affiche toute la config

    Args:
        cArgs (argparse.Namespace): paramètres utilisateurs
    """
    cParser = Config().get_parser()

    # Juste une section ou toute la config ?
    if cArgs.section is not None:
        # Juste une section
        if cArgs.option is not None:
            # On nous demande une section.option
            try:
                print(cParser.get(cArgs.section, cArgs.option))
            except configparser.NoSectionError as eNoSectionError:
                raise GpfApiError(f"La section '{cArgs.section}' n'existe pas dans la configuration.") from eNoSectionError
            except configparser.NoOptionError as eNoOptionError:
                raise GpfApiError(f"L'option '{cArgs.option}' n'existe pas dans la section '{cArgs.section}'.") from eNoOptionError
        else:
            # On nous demande toute une section
            try:
                # On crée un nouveau parser
                cParser2 = configparser.ConfigParser()
                # On y met la section demandée
                cParser2[cArgs.section] = cParser[cArgs.section]
                # On affiche tout ça
                with io.StringIO() as cStringIO:
                    cParser2.write(cStringIO)
                    cStringIO.seek(0)
                    print(cStringIO.read()[:-1])
            except KeyError as eKeyError:
                raise GpfApiError(f"La section '{cArgs.section}' n'existe pas dans la configuration.") from eKeyError
    else:
        # On nous demande toute la config
        if cArgs.file is not None:
            # On sauvegarde la donnée
            try:
                with open(cArgs.file, mode="w", encoding="UTF-8") as fIni:
                    cParser.write(fIni)
            except PermissionError as ePermissionError:
                raise GpfApiError(f"Impossible d'écrire le fichier {cArgs.file} : non autorisé") from ePermissionError
        else:
            # Sinon on l'affiche
            with io.StringIO() as cStringIO:
                cParser.write(cStringIO)
                cStringIO.seek(0)
                print(cStringIO.read()[:-1])


if __name__ == "__main__":
    try:
        main()
    except GpfApiError as eGpfApiError:
        print(eGpfApiError.message)
        sys.exit(1)
    except Exception as eException:
        print("Erreur non spécifiée à la création :")
        print(traceback.format_exc())
        sys.exit(1)
