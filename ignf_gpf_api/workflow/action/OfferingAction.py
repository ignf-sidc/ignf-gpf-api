from typing import Any, Dict, Optional

from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.Errors import ConflictError


class OfferingAction(ActionAbstract):
    """Classe dédiée à la création des Offering.

    Attributes:
        __workflow_context (str): nom du contexte du workflow
        __definition_dict (Dict[str, Any]): définition de l'action
        __parent_action (Optional["Action"]): action parente
        __offering (Optional[Offering]): représentation Python de la Offering créée
    """

    def __init__(self, workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
        super().__init__(workflow_context, definition_dict, parent_action)
        # Autres attributs
        self.__offering: Optional[Offering] = None

    def run(self, datastore: Optional[str]) -> None:
        Config().om.info("Création d'une offre...")
        # Ajout de l'Offering
        self.__create_offering(datastore)
        # Affichage
        o_offering = self.offering
        if o_offering is not None:
            # Récupération des liens
            o_offering.api_update()
            if len(o_offering["urls"]) > 0 and isinstance(o_offering["urls"][0], dict):
                # si les url sont récupérées sous forme de dict on affiche l'url uniquement
                s_urls = "\n   - ".join([d_url["url"] for d_url in o_offering["urls"]])
            else:
                # si les url sont récupérées sous forme de liste
                s_urls = "\n   - ".join(o_offering["urls"])
            Config().om.info(f"Offre créée : {self.__offering}\n{s_urls}")
        Config().om.info("Création d'une offre : terminé")

    def __create_offering(self, datastore: Optional[str]) -> None:
        """Création de l'Offering sur l'API à partir des paramètres de définition de l'action.

        Args:
            datastore (Optional[str]): id du datastore à utiliser.
        """
        o_offering = self.find_offering(datastore)
        if o_offering is not None:
            self.__offering = o_offering
            Config().om.info(f"Offre {self.__offering['layer_name']} déjà existante, complétion uniquement.")
        else:
            # Création en gérant une erreur de type ConflictError (si la Configuration existe déjà selon les critères de l'API)
            try:
                self.__offering = Offering.api_create(self.definition_dict["body_parameters"], route_params=self.definition_dict["url_parameters"])
            except ConflictError:
                Config().om.warning("L'offre que vous tentez de créer existe déjà !")

    def find_configuration(self, datastore: Optional[str]) -> Optional[Configuration]:
        """Fonction permettant de récupérer la Configuration associée à l'Offering qui doit être crée par cette Action.

        C'est à dire la Configuration indiquée dans `url_parameters` du `definition_dict` de cette Action.

        Args:
            datastore (Optional[str]): id du datastore à utiliser.
        Returns:
            Configuration
        """
        # Récupération de l'id de la configuration et du endpoint
        s_configuration_id = self.definition_dict["url_parameters"]["configuration"]
        # Instanciation Configuration
        o_configuration = Configuration.api_get(s_configuration_id, datastore=datastore)
        # Retour
        return o_configuration

    def find_offering(self, datastore: Optional[str]) -> Optional[Offering]:
        """Fonction permettant de récupérer l'Offering qui devrait être créée (si elle existe déjà).

        C'est à dire une offering associée à la Configuration indiquée dans `url_parameters` et au endpoint indiqué dans `body_parameters`.

        Args:
            datastore (Optional[str]): id du datastore à utiliser.
        Returns:
            Offre retrouvée
        """
        # Récupération de l'id de la configuration et du endpoint
        s_configuration_id = self.definition_dict["url_parameters"]["configuration"]
        s_endpoint_id = self.definition_dict["body_parameters"]["endpoint"]
        # Instanciation Configuration
        o_configuration = Configuration.api_get(s_configuration_id, datastore=datastore)
        # Listing des Offres associées à cette Configuration
        l_offerings = o_configuration.api_list_offerings()
        # Pour chaque offering
        for o_offering in l_offerings:
            # On récupère toutes les infos
            o_offering.api_update()
            # On regarde si elle est associée au bon endpoint
            if o_offering["endpoint"]["_id"] == s_endpoint_id:
                # On a notre offering, on sort !
                return o_offering
        # sinon on retourne None
        return None

    @property
    def offering(self) -> Optional[Offering]:
        return self.__offering
