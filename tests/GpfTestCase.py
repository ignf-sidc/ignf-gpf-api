import unittest
from unittest.mock import PropertyMock, patch, MagicMock

from ignf_gpf_api.io.Config import Config


class GpfTestCase(unittest.TestCase):
    """classe générique pour les tests"""

    _o_mock_om = None

    @classmethod
    def setUpClass(cls) -> None:
        """fonction lancer avant les testes sur la classe

        -> mock de om pour supprimé l'affichage
        """
        print("setup")
        o_el = patch.object(Config, "om", new_callable=PropertyMock)
        cls._o_mock_om = o_el.start()
        cls._o_mock_om.return_value = MagicMock()
