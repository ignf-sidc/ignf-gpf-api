from pathlib import Path

from ignf_gpf_api.store.StoreEntity import StoreEntity


class Upload(StoreEntity):
    """Classe Python représentant l'entité Upload (livraison)."""

    _entity_name = "upload"
    _entity_title = "livraison"

    def api_push_data_file(self, file_path: Path, api_path: str) -> None:
        """Envoie un fichier de donnée à la livraison.

        Args:
            file_path (Path): chemin local vers le fichier à envoyer
            api_path (str): dossier distant où déposer le fichier
        """
        raise NotImplementedError("Upload.api_push_data_file")

    def api_push_md5_file(self, file_path: Path) -> None:
        """Envoie un fichier md5 à la livraison.

        Args:
            file_path (Path): chemin local vers le fichier à envoyer
        """
        raise NotImplementedError("Upload.api_push_md5_file")

    def api_open(self) -> None:
        """Ouvre une livraison."""
        raise NotImplementedError("Upload.api_open")

    def api_close(self) -> None:
        """Ferme une livraison."""
        raise NotImplementedError("Upload.api_close")
