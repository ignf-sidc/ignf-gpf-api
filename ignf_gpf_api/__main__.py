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
from ignf_gpf_api.helper.JsonHelper import JsonHelper
from ignf_gpf_api.io.Errors import ConflictError
from ignf_gpf_api.workflow.Workflow import Workflow
from ignf_gpf_api.workflow.resolver.GlobalResolver import GlobalResolver
from ignf_gpf_api.workflow.resolver.StoreEntityResolver import StoreEntityResolver
from ignf_gpf_api.workflow.action.UploadAction import UploadAction
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.DescriptorFileReader import DescriptorFileReader
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.workflow.resolver.UserResolver import UserResolver


def main() -> None:
    """Fonction d'entrée."""
    # Résolution des paramètres utilisateurs
    o_args = parse_args()

    # Résolution de la config
    if not Path(o_args.config).exists():
        Config().om.warning(f"Le fichier de configuration précisé ({o_args.config}) n'existe pas.")
    Config().read(o_args.config)

    # Si debug on monte la config
    if o_args.debug:
        Config().om.set_log_level("DEBUG")

    # Exécution de l'action demandée
    if o_args.task == "auth":
        auth(o_args)
    elif o_args.task == "config":
        config(o_args)
    elif o_args.task == "upload":
        upload(o_args)
    elif o_args.task == "dataset":
        dataset(o_args)
    elif o_args.task == "workflow":
        workflow(o_args)


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
    o_parser.add_argument("--debug", dest="debug", required=False, default=False, action="store_true", help="Passe l'appli en mode debug (plus de messages affichés)")
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
    o_parser_auth.add_argument("--name", "-n", type=str, default=None, help="Nom du dataset à extraire")
    o_parser_auth.add_argument("--folder", "-f", type=str, default=None, help="Dossier où enregistrer le dataset")
    # Parser pour workflow
    o_parser_auth = o_sub_parsers.add_parser("workflow", help="Workflow")
    o_parser_auth.add_argument("--file", "-f", type=str, default=None, help="Chemin du fichier à utiliser OU chemin où extraire le dataset")
    o_parser_auth.add_argument("--name", "-n", type=str, default=None, help="Nom du workflow à extraire")
    o_parser_auth.add_argument("--step", "-s", type=str, default=None, help="Étape du workflow à lancer")
    o_parser_auth.add_argument("--behavior", "-b", type=str, default=None, help="Action à effectuer si l'exécution de traitement existe déjà")
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
            s_behavior = str(o_args.behavior).upper() if o_args.behavior is not None else None
            o_ua = UploadAction(o_dataset, behavior=s_behavior)
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
    """Liste les jeux de données d'exemple proposés et, si demandé par l'utilisateur, en export un.

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    p_root = Config.data_dir_path / "datasets"
    if o_args.name is not None:
        s_dataset = str(o_args.name)
        print(f"Exportation du jeu de donnée '{s_dataset}'...")
        p_from = p_root / s_dataset
        if p_from.exists():
            p_output = Path(o_args.folder) if o_args.folder is not None else Path(s_dataset)
            if p_output.exists():
                p_output = p_output / s_dataset
            print(f"Chemin de sortie : {p_output}")
            # Copie du répertoire
            shutil.copytree(p_from, p_output)
            print("Exportation terminée.")
        else:
            raise GpfApiError(f"Jeu de données '{s_dataset}' introuvable.")
    else:
        l_children: List[str] = []
        for p_child in p_root.iterdir():
            if p_child.is_dir():
                l_children.append(p_child.name)
        print("Jeux de données disponibles :\n   * {}".format("\n   * ".join(l_children)))


def workflow(o_args: argparse.Namespace) -> None:
    """Vérifie ou exécute un workflow.

    Args:
        o_args (argparse.Namespace): paramètres utilisateurs
    """
    p_root = Config.data_dir_path / "workflows"
    if o_args.name is not None:
        s_workflow = str(o_args.name)
        print(f"Exportation du workflow '{s_workflow}'...")
        p_from = p_root / s_workflow
        if p_from.exists():
            p_output = Path(o_args.file) if o_args.file is not None else Path(s_workflow)
            if p_output.exists() and p_output.is_dir():
                p_output = p_output / s_workflow
            print(f"Chemin de sortie : {p_output}")
            # Copie du répertoire
            shutil.copyfile(p_from, p_output)
            print("Exportation terminée.")
        else:
            raise GpfApiError(f"Workflow '{s_workflow}' introuvable.")
    elif o_args.file is not None:
        # Ouverture du fichier
        p_workflow = Path(o_args.file).absolute()
        Config().om.info(f"Ouverture du workflow {p_workflow}...")
        o_workflow = Workflow(p_workflow.stem, JsonHelper.load(p_workflow))
        # Y'a-t-il une étape d'indiquée
        if o_args.step is None:
            # Si pas d'étape indiquée, on valide le workflow
            Config().om.info("Validation du workflow...")
            l_errors = o_workflow.validate()
            if l_errors:
                s_errors = "\n   * ".join(l_errors)
                Config().om.error(f"{len(l_errors)} erreurs ont été trouvées dans le workflow.")
                Config().om.info(f"Liste des erreurs :\n   * {s_errors}")
                raise GpfApiError("Workflow invalide.")
            Config().om.info("Le workflow est valide.", green_colored=True)
        else:
            # Sinon, on définit des résolveurs
            GlobalResolver().add_resolver(StoreEntityResolver("store_entity"))
            GlobalResolver().add_resolver(UserResolver("user"))
            # et on lance l'étape
            s_behavior = str(o_args.behavior).upper() if o_args.behavior is not None else None
            o_workflow.run_step(o_args.step, print, behavior=s_behavior)
    else:
        l_children: List[str] = []
        for p_child in p_root.iterdir():
            if p_child.is_file():
                l_children.append(p_child.name)
        print("Jeux de données disponibles :\n   * {}".format("\n   * ".join(l_children)))


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except GpfApiError as e_gpf_api_error:
        Config().om.critical(e_gpf_api_error.message)
    except ConflictError:
        # gestion "globale" des ConflictError (ConfigurationAction et OfferingAction
        # possèdent chacune leur propre gestion)
        Config().om.critical("La requête envoyée à l'Entrepôt génère un conflit. N'avez-vous pas déjà effectué l'action que vous essayez de faire ?")
    except Exception as e_exception:
        Config().om.critical("Erreur non spécifiée :")
        Config().om.error(traceback.format_exc())
        Config().om.critical("Erreur non spécifiée.")
    sys.exit(1)
