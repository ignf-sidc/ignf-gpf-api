from typing import Any
from pathlib import Path
import unittest
from unittest.mock import PropertyMock, patch, MagicMock
import requests

import requests_mock

from ignf_gpf_api.io.Config import Config


class GpfTestCase(unittest.TestCase):
    """classe générique pour les tests"""

    _o_patch_om = None
    _o_mock_om = None

    conf_dir_path = Path(__file__).parent.absolute() / "_conf"
    data_dir_path = Path(__file__).parent.absolute() / "_data"
    test_dir_path = Path(__file__).parent.absolute() / "_test"

    @classmethod
    def setUpClass(cls) -> None:
        """fonction lancée une fois avant tous les tests de la classe
        -> mock de om pour supprimer l'affichage
        """
        print("setup")
        cls._o_patch_om = o_el = patch.object(Config, "om", new_callable=PropertyMock, return_value=MagicMock())
        cls._o_mock_om = o_el.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """fonction lancée une fois après tous les tests de la classe
        -> dé-mock de om pour stopper la suppression l'affichage
        """
        # On ne mock plus la classe d'authentification
        if cls._o_patch_om:
            cls._o_patch_om.stop()

    @staticmethod
    def get_response(**kwargs: Any) -> requests.Response:
        """Génère une réponse selon les arguments passés en paramètres.
        Args:
            **kwargs (Any): _description_
        Returns:
            requests.Response: _description_
        """
        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.get("http://test.com/", **kwargs)
            o_response = requests.request("GET", "http://test.com/")
            return o_response
