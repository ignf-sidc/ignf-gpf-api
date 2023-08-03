from unittest.mock import patch, MagicMock
from typing import Any

from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.OfferingAction import OfferingAction

from tests.GpfTestCase import GpfTestCase


class OfferingActionTestCase(GpfTestCase):
    """Tests OfferingAction class.

    cmd : python3 -m unittest -b tests.workflow.action.OfferingActionTestCase
    """

    # creation du dictionnaire qui reprend les paramètres du workflow pour créer une offre
    d_action = {"type": "offering", "body_parameters": {"endpoint": "id_endpoint"}, "url_parameters": {"configuration": "id_configuration"}}

    def __get_offering_action(self) -> OfferingAction:
        # Instanciation de OfferingAction
        o_offering_action = OfferingAction("contexte", self.d_action)
        # Retour
        return o_offering_action

    def test_run_not_existing(self) -> None:
        """test de run quand l'offre à créer n'existe pas"""
        # Instanciation de OfferingAction
        o_offering_action = self.__get_offering_action()

        # mock de offering
        o_mock_offering = MagicMock()
        o_mock_offering.api_launch.return_value = None

        # On mock find_offering et api_create
        with patch.object(o_offering_action, "find_offering", return_value=None) as o_mock_offering_action_list_offering:
            with patch.object(Offering, "api_create", return_value=o_mock_offering) as o_mock_offering_api_create:
                # on lance l'exécution de run
                o_offering_action.run()

                # test de l'appel à OfferingAction.find_offering
                o_mock_offering_action_list_offering.assert_called_once()

                # test de l'appel à Offering.api_create
                o_mock_offering_api_create.assert_called_once_with(self.d_action["body_parameters"], route_params=self.d_action["url_parameters"])

    # On mock find_offering et api_create
    def test_run_existing(self) -> None:
        """test de run quand l'offre à créer existe"""
        # Instanciation de OfferingAction
        o_offering_action = self.__get_offering_action()

        # mock de offering
        o_mock_offering = MagicMock()
        o_mock_offering.api_launch.return_value = None

        def side_effect_dict(arg: str) -> Any:
            """side_effect pour récupération des élément de offering, gestion du cas des url qui sont dans un dictionnaire

            Args:
                arg (str): clef à affiché

            Returns:
                Any: valeur de retour
            """
            if arg == "urls":
                return [{"url": "http://1"}, {"url": "http://2"}]
            return "getitem"

        def side_effect_text(arg: str) -> Any:
            """side_effect pour récupération des élément de offering, gestion du cas des url qui sont donné directement

            Args:
                arg (str): clef à affiché

            Returns:
                Any: valeur de retour
            """
            if arg == "urls":
                return ["http://1", "http://2"]
            return "getitem"

        for f_effect in [side_effect_dict, side_effect_text]:
            o_mock_offering.__getitem__.side_effect = f_effect

            with patch.object(o_offering_action, "find_offering", return_value=o_mock_offering) as o_mock_offering_action_list_offering:
                with patch.object(Offering, "api_create", return_value=None) as o_mock_offering_api_create:
                    # on lance l'exécution de run
                    o_offering_action.run()

                    # test de l'appel à OfferingAction.find_offering
                    o_mock_offering_action_list_offering.assert_called_once()

                    # test de l'appel à Offering.api_create
                    o_mock_offering_api_create.assert_not_called()

    def test_find_offering_exists_and_ok(self) -> None:
        """Test de find_offering quand une offering est trouvée et que le endpoint correspond.

        Dans ce test, on suppose que le datastore est défini.
        """

        # mock de Offering
        o_mock_offering = MagicMock()
        o_mock_offering.api_update.return_value = None
        o_mock_offering.__getitem__.return_value = {"_id": "id_endpoint"}

        # mock de Configuration
        o_mock_configuration = MagicMock()
        o_mock_configuration.api_list_offerings.return_value = [o_mock_offering]

        # Mock
        with patch.object(Configuration, "api_get", return_value=o_mock_configuration) as o_mock_api_get:
            # Instanciation de OfferingAction
            o_offering_action = self.__get_offering_action()
            # Appel à la fonction
            o_offering = o_offering_action.find_offering("datastore_id")
            # Vérifications
            o_mock_api_get.assert_called_once_with("id_configuration", datastore="datastore_id")
            o_mock_configuration.api_list_offerings.assert_called_once_with()
            o_mock_offering.api_update.assert_called_once()
            o_mock_offering.api_update.api_list_offerings()
            self.assertEqual(o_offering, o_mock_offering)

    def test_find_offering_exists_and_ko(self) -> None:
        """Test de find_offering quand une offering est trouvée mais que le endpoint ne correspond.

        Dans ce test, on suppose que le datastore est défini.
        """

        # mock de Offering
        o_mock_offering_ko = MagicMock()
        o_mock_offering_ko.api_update.return_value = None
        o_mock_offering_ko.__getitem__.return_value = {"_id": "id_endpoint_not_good"}

        # mock de Configuration
        o_mock_configuration_ko = MagicMock()
        o_mock_configuration_ko.api_list_offerings.return_value = [o_mock_offering_ko]

        # Mock
        with patch.object(Configuration, "api_get", return_value=o_mock_configuration_ko) as o_mock_api_get:
            # Instanciation de OfferingAction
            o_offering_action = self.__get_offering_action()
            # Appel à la fonction find_offering qui appelle les fonctions
            # mockées (api_get, api_list_offerings, api_update)
            o_offering = o_offering_action.find_offering("id_datastore_quelconque")

            # Vérifications ( sur find_offering() )
            # la Configuration.api_get() est bien appelée
            o_mock_api_get.assert_called_once_with("id_configuration", datastore="id_datastore_quelconque")
            # la liste des offres est correctement appelée
            o_mock_configuration_ko.api_list_offerings.assert_called_once()
            # les infos de l'offering sont correctement récupérées
            o_mock_offering_ko.api_update.assert_called_once()
            # aucune offre ne correspond au endpoint
            self.assertIsNone(o_offering)

    def test_find_offering_not_exists(self) -> None:
        """Test de find_offering quand aucune offering n'est trouvée.

        Dans ce test, on suppose que le datastore n'est pas défini.
        """
        # Instanciation de OfferingAction
        o_offering_action = self.__get_offering_action()

        # mock de Configuration
        o_mock_configuration = MagicMock()
        o_mock_configuration.api_list_offerings.return_value = []

        # Mock
        with patch.object(Configuration, "api_get", return_value=o_mock_configuration) as o_mock_api_get:
            # Appel à la fonction
            o_offering = o_offering_action.find_offering()
            # Vérifications
            o_mock_api_get.assert_called_once_with("id_configuration", datastore=None)
            o_mock_configuration.api_list_offerings.assert_called_once()
            self.assertIsNone(o_offering)

    def test_find_configuration(self) -> None:
        """Test de find_configuration."""
        # Instanciation de OfferingAction
        o_offering_action = self.__get_offering_action()

        # mock de Configuration
        o_mock_configuration = MagicMock()

        # Mock 1 : trouvée
        with patch.object(Configuration, "api_get", return_value=o_mock_configuration) as o_mock_api_get:
            # Appel à la fonction
            o_configuration = o_offering_action.find_configuration()
            # Vérifications
            o_mock_api_get.assert_called_once_with("id_configuration", datastore=None)
            self.assertEqual(o_configuration, o_mock_configuration)

        # Mock 2 : non trouvée
        with patch.object(Configuration, "api_get", return_value=None) as o_mock_api_get:
            # Appel à la fonction
            o_configuration = o_offering_action.find_configuration()
            # Vérifications
            o_mock_api_get.assert_called_once_with("id_configuration", datastore=None)
            self.assertIsNone(o_configuration)
