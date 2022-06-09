"""API Python pour simplifier l'utilisation de l'API Entrepôt Géo-plateforme."""

import configparser
import io
import sys
import argparse
import traceback
from pathlib import Path
from typing import List, Optional, Sequence
import shutil

import ignf_gpf_api
from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.auth.Authentifier import Authentifier
from ignf_gpf_api.workflow.action.UploadAction import UploadAction
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.DescriptorFileReader import DescriptorFileReader
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.store.StoreEntity import StoreEntity


def main() -> None:
    """Fonction d'entrée."""
    # Résolution des paramètres utilisateurs
    o_args = parse_args()

    # Résolution de la config
    if not Path(o_args.config).exists():
        raise GpfApiError(f"Le fichier de configuration précisé ({o_args.config}) n'existe pas.")
    Config().read(o_args.config)

    # Exécution de l'action demandée
    if o_args.task == "auth":
        auth(o_args)
    elif o_args.task == "config":
        config(o_args)
    elif o_args.task == "upload":
        upload(o_args)
    elif o_args.task == "dataset":
        dataset(o_args)


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse les paramètres utilisateurs.

    Args:
        args (Optional[Sequence[str]], optional): paramètres à parser, si None sys.argv utilisé. Defaults to None.

    Returns:
        argparse.Namespace: paramètres
    """
    # Parsing des paramètres
    o_parser = argparse.ArgumentParser(prog="ignf_gpf_api", description="Exécutable pour interagir avec l'API Entrepôt de la Géoplateforme.")
    o_parser.add_argument("--ini", dest="config", default="config.ini", help="Chemin vers le fichier de config à utiliser (config.ini par défaut)")
    o_parser.add_argument("--version", action="version", version=f"%(prog)s v{ignf_gpf_api.__version__}")
    o_sub_parsers = o_parser.add_subparsers(dest="task", metavar="TASK", required=True, help="Tâche à effectuer")
    # Parser pour auth
    o_parser_auth = o_sub_parsers.add_parser("auth", help="Authentification")
    o_parser_auth.add_argument("--show", type=str, choices=["token", "header"], default=None, help="Donnée à renvoyer")
    # Parser pour config
    o_parser_auth = o_sub_parsers.add_parser("config", help="Configuration")
    o_parser_auth.add_argument("--file", "-f", type=str, default=None, help="Chemin du fichier où sauvegarder la configuration (si null, la configuration est affichée)")
    o_parser_auth.add_argument("--section", "-s", type=str, default=None, help="Se limiter à une section")
    o_parser_auth.add_argument("--option", "-o", type=str, default=None, help="Se limiter à une option (section doit être renseignée)")
    # Parser pour upload
    o_parser_auth = o_sub_parsers.add_parser("upload", help="Livraisons")
    o_parser_auth.add_argument("--file", "-f", type=str, default=None, help="Chemin vers le fichier descriptor dont on veut effectuer la livraison)")
    o_parser_auth.add_argument("--infos", "-i", type=str, default=None, help="Filter les livraisons selon les infos")
    o_parser_auth.add_argument("--tags", "-t", type=str, default=None, help="Filter les livraisons selon les tags")
    o_parser_auth.add_argument("--behavior", "-b", type=str, default=None, help="Action à effectuer si la livraison existe déjà")
    o_parser_auth.add_argument("--id", type=str, default=None, help="Affiche la livraison demandée")
    # Parser pour dataset
    o_parser_auth = o_sub_parsers.add_parser("dataset", help="Jeux de données")
    o_parser_auth.add_argument("--name", "-n", type=str, default=None, help="Nom du dataset à enregistrer")
    o_parser_auth.add_argument("--file", "-f", type=str, default=None, help="Chemin du fichier descriptor à créer")
    return o_parser.parse_args(args)


def auth(o_args: argparse.Namespace) -> None:
    """Authentifie l'utilisateur et retourne les informations de connexion demandées.
    Si aucune information est demandée, confirme juste la bonne authentification.

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    s_token = Authentifier().get_access_token_string()
    if o_args.show == "token":
        print(s_token)
    elif o_args.show == "header":
        print(Authentifier().get_http_header())
    else:
        print("Authentification réussie.")


def config(o_args: argparse.Namespace) -> None:
    """Fonction pour afficher ou sauvegarder la configuration :
    * si une section (voire une option) est demandée, on affiche ce qui est demandé
    * sinon :
        * si un fichier est précisé on y enregistre toute la config
        * sinon on affiche toute la config

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    o_parser = Config().get_parser()

    # Juste une section ou toute la config ?
    if o_args.section is not None:
        # Juste une section
        if o_args.option is not None:
            # On nous demande une section.option
            try:
                print(o_parser.get(o_args.section, o_args.option))
            except configparser.NoSectionError as e_no_section_error:
                raise GpfApiError(f"La section '{o_args.section}' n'existe pas dans la configuration.") from e_no_section_error
            except configparser.NoOptionError as e_no_option_error:
                raise GpfApiError(f"L'option '{o_args.option}' n'existe pas dans la section '{o_args.section}'.") from e_no_option_error
        else:
            # On nous demande toute une section
            try:
                # On crée un nouveau parser
                o_parser2 = configparser.ConfigParser()
                # On y met la section demandée
                o_parser2[o_args.section] = o_parser[o_args.section]
                # On affiche tout ça
                with io.StringIO() as o_string_io:
                    o_parser2.write(o_string_io)
                    o_string_io.seek(0)
                    print(o_string_io.read()[:-1])
            except KeyError as e_key_error:
                raise GpfApiError(f"La section '{o_args.section}' n'existe pas dans la configuration.") from e_key_error
    else:
        # On nous demande toute la config
        if o_args.file is not None:
            # On sauvegarde la donnée
            try:
                with open(o_args.file, mode="w", encoding="UTF-8") as f_ini:
                    o_parser.write(f_ini)
            except PermissionError as e_permission_error:
                raise GpfApiError(f"Impossible d'écrire le fichier {o_args.file} : non autorisé") from e_permission_error
        else:
            # Sinon on l'affiche
            with io.StringIO() as o_string_io:
                o_parser.write(o_string_io)
                o_string_io.seek(0)
                print(o_string_io.read()[:-1])


def upload(o_args: argparse.Namespace) -> None:
    """Création/Gestion des Livraison (Upload).
    Si un fichier descriptor est précisé, on effectue la livraison.
    Si un id est précisé, on affiche la livraison.
    Sinon on liste les Livraisons avec éventuellement des filtres.

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    if o_args.file is not None:
        p_file = Path(o_args.file)
        o_dfu = DescriptorFileReader(p_file)
        for o_dataset in o_dfu.datasets:
            o_ua = UploadAction(o_dataset, behavior=o_args.behavior)
            o_upload = o_ua.run()
            if UploadAction.monitor_until_end(o_upload, print):
                print(f"Livraison {o_upload} créée avec succès.")
            else:
                print(f"Livraison {o_upload} créée en erreur !")
    elif o_args.id is not None:
        o_upload = Upload.api_get(o_args.id)
        print(o_upload)
    else:
        d_infos_filter = StoreEntity.filter_dict_from_str(o_args.infos)
        d_tags_filter = StoreEntity.filter_dict_from_str(o_args.tags)
        l_uploads = Upload.api_list(infos_filter=d_infos_filter, tags_filter=d_tags_filter)
        for o_upload in l_uploads:
            print(o_upload)


def dataset(o_args: argparse.Namespace) -> None:
    """List les jeux de données test proposés et si demandé en export un.

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    p_root = Path(__file__).parent.parent / "tests" / "_data" / "test_datasets"
    if o_args.name is not None:
        print(f"Exportation du jeux de donnée '{o_args.name}'...")
        p_output = Path(o_args.file) if o_args.file is not None else Path(f"{o_args.name}.json")
        print(f"Chemin de sortie : {p_output}")
        # Copie du fichier JSON
        p_from = p_root / f"{o_args.name}.json"
        shutil.copy(p_from, p_output)
        # Copie du répertoire
        shutil.copytree(p_from.with_suffix(""), p_output.with_suffix(""))
        print("Exportation terminée.")
    else:
        l_children: List[str] = []
        for p_child in p_root.iterdir():
            if p_child.is_dir():
                l_children.append(p_child.name)
        print("Jeux de données disponibles :\n   * {}".format("\n   * ".join(l_children)))


if __name__ == "__main__":
    try:
        main()
    except GpfApiError as e_gpf_api_error:
        print(e_gpf_api_error.message)
        sys.exit(1)
    except Exception as e_exception:
        print("Erreur non spécifiée :")
        print(traceback.format_exc())
        sys.exit(1)
