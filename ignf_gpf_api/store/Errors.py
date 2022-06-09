from ignf_gpf_api.Errors import GpfApiError


class StoreEntityError(GpfApiError):
    """Est levée quand un problème apparaît durant une opération sur une StoreEntity."""
