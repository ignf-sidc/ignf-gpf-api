from pathlib import Path

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.StoreEntity import StoreEntity


class ReUploadFileInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les entités mises à jour par le téléversement d'un fichier."""

    def api_re_upload(self, file: Path) -> None:
        """Reupload le fichier l'entité sur l'API (PUT).

        Args:
            file (Path): nom du ficher à upload
        """

        # Génération du nom de la route
        s_route = f"{self._entity_name}_re_upload"

        # nom de la clef dans le fichier
        s_file_key = Config().get_str(self._entity_name, "create_file_key")

        # Requête
        ApiRequester().route_upload_file(
            s_route,
            file,
            s_file_key,
            method=ApiRequester.PUT,
        )

        # Mise à jour du stockage local (_store_api_dict)
        self.api_update()
