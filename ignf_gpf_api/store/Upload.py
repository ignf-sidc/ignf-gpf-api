from pathlib import Path

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.TagInterface import TagInterface
from ignf_gpf_api.store.CommentInterface import CommentInterface
from ignf_gpf_api.store.SharingInterface import SharingInterface
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError


class Upload(TagInterface, CommentInterface, SharingInterface, StoreEntity):
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

    def is_open(self) -> bool:
        """Test si la livraison est ouverte

        Returns:
            bool: si livraison ouverte
        """
        self.api_update()
        if "status" not in self._store_api_dict:
            raise StoreEntityError("Impossible de récupérer le status de l'upload")
        return bool(Config().get("upload_status", "open_status") == self["status"])
