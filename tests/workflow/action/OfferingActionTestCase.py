import unittest
from unittest.mock import patch, MagicMock

from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.workflow.action.OfferingAction import OfferingAction


# pylint:disable=too-many-arguments
# pylint:disable=too-many-locals
# pylint:disable=too-many-branches
# fmt: off
class OfferingActionTestCase(unittest.TestCase):
    """Tests OfferingAction class.
    cmd : python3 -m unittest -b tests.workflow.action.OfferingActionTestCase
    """

    def test_run(self) -> None:
        """test de run"""
        # creation du dictionnaire qui reprend les paramétres du workflow pour creer une offre
        d_action = {"type": "offering", "parameters": {"param": "valeur"}, "url_parameters": {"id_configuration"}}

        # initialisation de Offering
        o_offering = OfferingAction("contexte", d_action)

        # mock de offering
        o_mock_offering = MagicMock()
        o_mock_offering.api_launch.return_value = None


        # suppression de la mise en page forcé pour le with
        with patch.object(Offering, "api_create", return_value=o_mock_offering) as o_mock_offering_api_create :
            # on lance l'exécution de run
            o_offering.run()

            # test de l'appel à Offering.api_create
            o_mock_offering_api_create.assert_called_once_with(d_action['parameters'], route_params=d_action['url_parameters'])
