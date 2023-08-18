from pathlib import Path
from typing import Optional

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class DownloadInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les téléchargements"""

    def api_download(self, file_path: Path, datastore: Optional[str] = None) -> None:
        """Télécharge le Fichier Statique et l'enregistre localement.

        Args:
            file_path: chemin local où enregistrer le fichier
            datastore (Optional[str]): id du datastore à utiliser. Si None, le datastore sera récupéré dans configuration. Defaults to None.
        """
        if not datastore:
            datastore = self.datastore

        s_route = f"{self._entity_name}_download"
        # Requête "get" à l'API
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id, "datastore": datastore},
        )

        with file_path.open("wb", encoding="UTF-8") as o_out_file:
            o_out_file.write(o_response.content)
