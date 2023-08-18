from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.store.interface.ReUploadFileInterface import ReUploadFileInterface
from ignf_gpf_api.store.interface.DownloadInterface import DownloadInterface
from ignf_gpf_api.store.interface.CreatedByUploadFileInterface import CreatedByUploadFileInterface


class Static(CreatedByUploadFileInterface, DownloadInterface, PartialEditInterface, ReUploadFileInterface, StoreEntity):
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
