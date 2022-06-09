from pathlib import Path
from typing import Any
import jsonschema  # type: ignore
from jsonc_parser.parser import JsoncParser  # type: ignore
from jsonc_parser.errors import ParserError  # type: ignore
from beartype._decor.main import beartype

from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.helper.FileHelper import FileHelper


class JsonHelper:
    """Classe d'aide pour gérer les fichiers JSON."""

    @staticmethod
    @beartype
    def load(
        json_path: Path,
        file_not_found_pattern: str = "Fichier JSON {json_path} non trouvé",
        file_not_parsable_pattern: str = "Fichier JSON {json_path} non parsable : {error}",
        encoding: str = "utf-8",
    ) -> Any:
        """Ouverture et parsing d'un fichier json

        Arguments:
            json_path (Path): chemin vers le fichier à ouvrir
            file_not_found_pattern (str): pattern du message à générer si fichier non trouvé
            file_not_parsable_pattern (str): pattern du message à générer si échec du parsing
            encoding (str): encodage du fichier (utf-8 par défaut)

        Raises:
            GpfApiError: levée si le parsing échoue.

        Returns:
            str: json contenu dans le fichier
        """
        try:
            s_data = FileHelper.read(json_path, file_not_found_pattern.replace("json_path", "path"), encoding=encoding)
            return JsoncParser.parse_str(s_data)
        except ParserError as e_json_decode_error:
            s_message = file_not_parsable_pattern.format(
                json_path=json_path,
                error=e_json_decode_error,
            )
            raise GpfApiError(s_message) from e_json_decode_error

    @staticmethod
    @beartype
    def loads(str_data: str, title: str, message_pattern: str = "Impossible de parser le JSON «{title}» : {error}\n{str_data}") -> Any:
        """Parse du JSON avec un message indiquant d'où vient l'erreur si jamais cela échoue

        Arguments:
            str_data (str): données en texte
            title (str): intitulé du json à parser
            message_pattern (str): pattern du message d'erreur à générer

        Raises:
            GpfApiError: levée si les données ne sont pas parsables

        Returns:
            Any: données en objet python
        """
        try:
            o_data = JsoncParser.parse_str(str_data)
            return o_data
        except ParserError as e_json_decode_error:
            s_message = message_pattern.format(
                title=title,
                error=e_json_decode_error,
                str_data=str_data,
            )
            raise GpfApiError(s_message) from e_json_decode_error

    @staticmethod
    @beartype
    def validate_json(
        json_path: Path,
        schema_path: Path,
        schema_not_found_pattern: str = "Le schéma JSON {schema_path} n'existe pas. Contactez le support.",
        schema_not_parsable_pattern: str = "Le schéma JSON {schema_path} n'est pas parsable. Contactez le support.",
        schema_not_valid_pattern: str = "Le schéma JSON {schema_path} n'est pas valide. Contactez le support.",
        json_not_found_pattern: str = "Le fichier JSON {json_path} n'existe pas. Contactez le support.",
        json_not_parsable_pattern: str = "Le fichier JSON {json_path} n'est pas parsable. Contactez le support.",
        json_not_valid_pattern: str = "Le fichier JSON {json_path} n'est pas valide. Contactez le support.",
    ) -> None:
        """Fonction de validation d'un fichier json face à un schéma JSON.

        Args:
            json_path (Path): Chemin du fichier à valider
            schema_path (Path): Chemin du fichier de schéma
            schema_not_found_pattern (str, optional): Pattern du message à afficher si le schéma n'est pas trouvé. Par défaut "Le schéma JSON {schema_path} n'existe pas.".
            schema_not_parsable_pattern (str, optional): Pattern du message à afficher si le schéma n'est pas parsable. Par défaut "Le schéma JSON {schema_path} n'est pas parsable.".
            schema_not_valid_pattern (str, optional): Pattern du message à afficher si le schéma n'est pas valide. Par défaut "Le schéma JSON {schema_path} n'est pas valide.".
            json_not_found_pattern (str, optional): Pattern du message à afficher si le json n'est pas trouvé. Par défaut "Le fichier JSON {json_path} n'existe pas.".
            json_not_parsable_pattern (str, optional): Pattern du message à afficher si le json n'est pas parsable. Par défaut "Le fichier JSON {json_path} n'est pas parsable.".
            json_not_valid_pattern (str, optional): Pattern du message à afficher si le json n'est pas valide. Par défaut "Le fichier JSON {json_path} n'est pas valide.".

        Raises:
            GpfApiError: levée si le json n'est pas trouvé
            GpfApiError: levée si le schéma n'est pas trouvé
            GpfApiError: levée si le schéma n'est pas valide
            GpfApiError: levée si le json n'est pas valide
        """
        # Chargement du json
        o_json_data = JsonHelper.load(
            json_path,
            file_not_found_pattern=json_not_found_pattern,
            file_not_parsable_pattern=json_not_parsable_pattern,
        )

        # Chargement du schéma
        o_schema_data = JsonHelper.load(
            schema_path,
            file_not_found_pattern=schema_not_found_pattern.replace("schema_path", "json_path"),
            file_not_parsable_pattern=schema_not_parsable_pattern.replace("schema_path", "json_path"),
        )

        # Validation
        s_message_schema = schema_not_valid_pattern.format(schema_path=schema_path)
        s_message_json = json_not_valid_pattern.format(json_path=json_path)
        JsonHelper.validate_object(o_json_data, o_schema_data, s_message_json, s_message_schema)

    @staticmethod
    @beartype
    def validate_object(json_data: object, schema_data: object, json_not_valid_message: str, schema_not_valid_message: str) -> None:
        """Fonction de validation d'un fichier json face à un schéma JSON.

        Args:
            json_data (object): donnée à valider
            schema_data (object): schéma de validation
            json_not_valid_message (str): message à afficher si le json n'est pas valide
            schema_not_valid_message (str): message à afficher si le schéma n'est pas valide

        Raises:
            GpfApiError: levée si le schéma n'est pas valide
            GpfApiError: levée si le json n'est pas valide
        """
        # Validation
        try:
            jsonschema.validate(instance=json_data, schema=schema_data)
        # Récupération de l'erreur levée si le schéma est invalide
        except jsonschema.exceptions.SchemaError as e:
            raise GpfApiError(schema_not_valid_message) from e
        # Récupération de l'erreur levée si le json est invalide
        except jsonschema.exceptions.ValidationError as e:
            raise GpfApiError(json_not_valid_message) from e
