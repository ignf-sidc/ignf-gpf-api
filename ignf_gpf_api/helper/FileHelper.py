from pathlib import Path
from ignf_gpf_api.Errors import GpfApiError


class FileHelper:
    """Classe d'aide pour gérer les fichiers."""

    @staticmethod
    def read(file_path: Path, file_not_found_pattern: str = "Fichier {path} non trouvé", encoding: str = "utf8") -> str:
        """Lit et retourne le contenu d'un fichier.

        Args:
            file_path (Path): chemin vers le fichier
            file_not_found_pattern (str, optional): Pattern du messsage d'erreur si fichier non trouvé. Defaults to "Fichier {path} non trouvé".
            encoding (str, optional): encodage du fichier. Defaults to "utf8".

        Raises:
            GpfApiError: levée si le fichier n'existe pas.

        Returns:
            str: le contenu du fichier
        """
        try:
            with file_path.open(encoding=encoding) as f_file:
                return f_file.read()
        except FileNotFoundError as e_fnf_error:
            raise GpfApiError(file_not_found_pattern.format(path=file_path)) from e_fnf_error
