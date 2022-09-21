from datetime import datetime
from unittest.mock import patch

from ignf_gpf_api.store.interface.CsfInterface import CsfInterface
from tests.GpfTestCase import GpfTestCase


class CsfInterfaceTestCase(GpfTestCase):
    """Tests CsfInterface class.

    cmd : python3 -m unittest -b tests.store.interface.CsfInterfaceTestCase
    """

    def test_creation(self) -> None:
        """Vérifie le bon fonctionnement de creation."""
        # Instanciation
        o_processing_execution = CsfInterface({"_id": "id_entité"})
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_processing_execution, "_get_datetime", return_value=datetime.now()) as o_mock_get_datetime:
            # on appelle la fonction à tester : launch
            o_datetime = o_processing_execution.creation

            # on vérifie que route_request est appelé correctement
            o_mock_get_datetime.assert_called_once_with("creation")
            self.assertEqual(o_datetime, o_mock_get_datetime.return_value)

    def test_start(self) -> None:
        """Vérifie le bon fonctionnement de start."""
        # Instanciation
        o_processing_execution = CsfInterface({"_id": "id_entité"})
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_processing_execution, "_get_datetime", return_value=datetime.now()) as o_mock_get_datetime:
            # on appelle la fonction à tester : start
            o_datetime = o_processing_execution.start

            # on vérifie que route_request est appelé correctement
            o_mock_get_datetime.assert_called_once_with("start")
            self.assertEqual(o_datetime, o_mock_get_datetime.return_value)

    def test_finish(self) -> None:
        """Vérifie le bon fonctionnement de finish."""
        # Instanciation
        o_processing_execution = CsfInterface({"_id": "id_entité"})
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_processing_execution, "_get_datetime", return_value=datetime.now()) as o_mock_get_datetime:
            # on appelle la fonction à tester : finish
            o_datetime = o_processing_execution.finish

            # on vérifie que route_request est appelé correctement
            o_mock_get_datetime.assert_called_once_with("finish")
            self.assertEqual(o_datetime, o_mock_get_datetime.return_value)
