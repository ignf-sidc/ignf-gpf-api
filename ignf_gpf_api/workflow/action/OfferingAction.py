from typing import Any, Dict, Optional
from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.io.Config import Config


class OfferingAction(ActionAbstract):
    """Classe dédiée à la création des Offering.

    Attributes :
        __workflow_context (str) : nom du contexte du workflow
        __definition_dict (Dict[str, Any]) : définition de l'action
        __parent_action (Optional["Action"]) : action parente
        __offering (Optional[Offering]) : représentation Python de la Offering créée
    """

    def __init__(self, workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
        super().__init__(workflow_context, definition_dict, parent_action)
        # Autres attributs
        self.__offering: Optional[Offering] = None

    def run(self) -> None:
        Config().om.info("Création d'une offre...")
        # Ajout de l'Offering
        self.__create_offering()
        # Affichage
        Config().om.info(f"Offre créée : {self.__offering}")
        Config().om.info("Création d'une offre : terminé")

    def __create_offering(self) -> None:
        """Création de l'Offering sur l'API à partir des paramètres de définition de l'action."""
        self.__offering = Offering.api_create(self.definition_dict["body_parameters"], route_params=self.definition_dict["url_parameters"])

    @property
    def offering(self) -> Optional[Offering]:
        return self.__offering
