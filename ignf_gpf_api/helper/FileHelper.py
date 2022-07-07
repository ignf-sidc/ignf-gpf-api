from pathlib import Path
import hashlib

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

    @staticmethod
    def format_size(size: int) -> str:
        """Return the given bytes as a human friendly KB, MB, GB, or TB string.
        cf. https://stackoverflow.com/a/31631711/7812850

        Args:
            size (int): taille en octet

        Returns:
            str: taille formatée
        """
        f_size_in_bytes = float(size)
        f_size_kb = float(1024)
        f_size_mb = float(f_size_kb**2)  # 1,048,576
        f_size_gb = float(f_size_kb**3)  # 1,073,741,824
        f_size_tb = float(f_size_kb**4)  # 1,099,511,627,776

        if f_size_in_bytes < f_size_kb:
            s_unit = "octets" if f_size_in_bytes > 1 else "octet"
            return f"{f_size_in_bytes:.0f} {s_unit}"
        if f_size_kb <= f_size_in_bytes < f_size_mb:
            return f"{f_size_in_bytes / f_size_kb:.2f} KO"
        if f_size_mb <= f_size_in_bytes < f_size_gb:
            return f"{f_size_in_bytes / f_size_mb:.2f} MO"
        if f_size_gb <= f_size_in_bytes < f_size_tb:
            return f"{f_size_in_bytes / f_size_gb:.2f} GO"
        return f"{f_size_in_bytes / f_size_tb:.2f} TO"

    @staticmethod
    def md5_hash(file_path: Path) -> str:
        """
        Méthode permettant de calculer la clef md5 d'un fichier

        Args:
            file_path (Path): chemin d'un fichier

        Returns:
            str: clef md5 du fichier
        """
        s_file_hash = hashlib.md5()
        with file_path.open("rb") as o_file:
            for o_chunk in iter(lambda: o_file.read(4096), b""):
                s_file_hash.update(o_chunk)
        return s_file_hash.hexdigest()
