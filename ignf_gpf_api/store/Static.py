from pathlib import Path
from typing import Optional

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.TagInterface import TagInterface
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.store.interface.FullEditInterface import FullEditInterface


class Static(TagInterface, PartialEditInterface, FullEditInterface, StoreEntity):
    """Classe Python représentant l'entité Fichier statique (static).

    Cette classe permet d'effectuer les actions spécifiques liées aux fichiers statiques : création,
    remplacement, mise à jour, suppression.
    """

    _entity_name = "static"
    _entity_title = "fichier statique"

    TYPE_GEOSERVER_FTL = "GEOSERVER-FTL"
    TYPE_GEOSERVER_STYLE = "GEOSERVER-STYLE"
    TYPE_ROK4_STYLE = "ROK4-STYLE"
    TYPE_DERIVATION_SQL = "DERIVATION-SQL"

    def api_download(self, file_path: Path, datastore: Optional[str] = None) -> None:
        """Télécharge le Fichier Statique et l'enregistre localement.

        Args:
            file_path: chemin local où enregistrer le fichier
            datastore (Optional[str]): id du datastore à utiliser. Si None, le datastore sera récupéré dans configuration. Defaults to None.
        """
        raise NotImplementedError("Fonction « Téléchargement fichier statique » non implémentée.")
