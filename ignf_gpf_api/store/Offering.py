from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface


class Offering(PartialEditInterface, StoreEntity):
    """Classe Python représentant l'entité Offering (offre)."""

    _entity_name = "offering"
    _entity_title = "offre"

    STATUS_PUBLISHING = "PUBLISHING"
    STATUS_MODIFYING = "MODIFYING"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_UNPUBLISHING = "UNPUBLISHING"
    STATUS_UNSTABLE = "UNSTABLE"

    VISIBILITY_PRIVATE = "PRIVATE"
    VISIBILITY_REFERENCED = "REFERENCED"
    VISIBILITY_PUBLIC = "PUBLIC"
