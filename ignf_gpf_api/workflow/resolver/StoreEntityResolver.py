import re
from typing import Dict, Optional, Pattern, Type

from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import NoEntityFoundError, ResolverError
from ignf_gpf_api.store.interface.TagInterface import TagInterface
from ignf_gpf_api.store.Processing import Processing
from ignf_gpf_api.store.StoredData import StoredData
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution
from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.store.Endpoint import Endpoint
from ignf_gpf_api.io.Config import Config


class StoreEntityResolver(AbstractResolver):
    """Classe permettant de résoudre des paramètres clé -> valeur.

    Attributes :
        __name (str): nom de code du resolver
        __regex (Pattern[str]): regex du resolver
    """

    __key_to_cls: Dict[str, Type[StoreEntity]] = {
        Upload.entity_name(): Upload,
        Processing.entity_name(): Processing,
        StoredData.entity_name(): StoredData,
        Configuration.entity_name(): Configuration,
        Offering.entity_name(): Offering,
        ProcessingExecution.entity_name(): ProcessingExecution,
        Endpoint.entity_name(): Endpoint,
    }

    def __init__(self, name: str) -> None:
        """Constructeur.

        Args:
            name (str): nom du résolveur
        """
        super().__init__(name)
        self.__regex: Pattern[str] = re.compile(Config().get("workflow_resolution_regex", "store_entity_regex"))

    def resolve(self, string_to_solve: str) -> str:
        # On parse la chaîne à résoudre
        o_result = self.regex.search(string_to_solve)
        if o_result is None:
            raise ResolverError(self.name, string_to_solve)
        d_groups = o_result.groupdict()
        # On récupère les filtres à utiliser
        # Sur les infos
        s_filter_infos: Optional[str] = d_groups["filter_infos"]
        d_filter_infos = StoreEntity.filter_dict_from_str(s_filter_infos)
        # Sur les tags
        s_filter_tags: Optional[str] = d_groups["filter_tags"]
        d_filter_tags = StoreEntity.filter_dict_from_str(s_filter_tags)
        # On récupère le type de StoreEntity demandé
        s_entity_type = str(d_groups["entity_type"])
        # On liste les éléments API via la fonction de classe
        l_entities = self.__key_to_cls[s_entity_type].api_list(infos_filter=d_filter_infos, tags_filter=d_filter_tags, page=1)
        # Si on a aucune entité trouvée
        if len(l_entities) == 0:
            raise NoEntityFoundError(self.name, string_to_solve)
        # Sinon on regarde ce qu'on doit envoyer
        o_entity = l_entities[0]
        s_selected_field = d_groups["selected_field"]
        # On doit envoyer une info ?
        if d_groups["selected_field_type"] == "infos":
            # On doit renvoyer une info
            return str(o_entity[s_selected_field])
        # On doit renvoyer un tag, possible que si ça implémente TagInterface
        if isinstance(o_entity, TagInterface):
            return o_entity.get_tag(s_selected_field)
        raise ResolverError(self.name, string_to_solve)

    @property
    def regex(self) -> Pattern[str]:
        return self.__regex
