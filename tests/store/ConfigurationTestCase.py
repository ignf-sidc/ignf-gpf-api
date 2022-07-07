from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.store.StoreEntity import StoreEntity

from tests.GpfTestCase import GpfTestCase


class ConfigurationTestCase(GpfTestCase):
    """Tests Configuration class.

    cmd : python3 -m unittest -b tests.store.ConfigurationTestCase
    """

    def test_list_offerings(self) -> None:
        """Vérifie le bon fonctionnement de api_list_offerings."""

        # Instanciation d'une fausse réponse HTTP
        o_response = GpfTestCase.get_response(json=[{"_id": "offering_1"}, {"_id": "offering_2"}])

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # Instanciation d'une Configuration
            o_configuration = Configuration({"_id": "123456789"})
            # Listing de ses Offres
            l_offerings = o_configuration.api_list_offerings()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "configuration_list_offerings",
                route_params={"configuration": "123456789"},
                method=ApiRequester.GET,
            )
            # on vérifie qu'on a bien récupéré une liste d'Offering
            self.assertIsInstance(l_offerings, list)
            self.assertIsInstance(l_offerings[0], Offering)
            self.assertIsInstance(l_offerings[1], Offering)
            self.assertEqual(l_offerings[0].id, "offering_1")
            self.assertEqual(l_offerings[1].id, "offering_2")

    def test_add_offering(self) -> None:
        """Vérifie le bon fonctionnement de api_add_offering."""

        d_data_offering = {"_id": "11111111"}

        # On mock la fonction api_create, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(StoreEntity, "api_create", return_value=Offering(d_data_offering)) as o_mock_create:
            # Instanciation d'une Configuration
            o_configuration = Configuration({"_id": "2222222"})
            # Ajout d'une Offre
            o_offering = o_configuration.api_add_offering(d_data_offering)
            # on vérifie que api_create est appelé correctement
            o_mock_create.assert_called_once_with(
                d_data_offering,
                route_params={"configuration": "2222222"},
            )
            # on vérifie que l'entité renvoyée est cohérente
            self.assertIsInstance(o_offering, Offering)
            self.assertEqual(o_offering.id, "11111111")
            self.assertDictEqual(o_offering.get_store_properties(), d_data_offering)
