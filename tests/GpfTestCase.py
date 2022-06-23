import unittest
from unittest.mock import PropertyMock, patch, MagicMock

from ignf_gpf_api.io.Config import Config


class GpfTestCase(unittest.TestCase):
    """classe générique pour les tests"""

    _o_patch_om = None
    _o_mock_om = None

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
