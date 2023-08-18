from ignf_gpf_api.store.AbstractCommonFile import AbstractCommonFile
from ignf_gpf_api.store.Errors import StoreEntityError

from tests.GpfTestCase import GpfTestCase


class RealCommonFile(AbstractCommonFile):
    """Classe réel pour AbstractCommonFile"""

    _entity_title = "real_common_file"


class AbstractCommonFileTestCase(GpfTestCase):
    """Tests AbstractCommonFile class.

    cmd : python3 -m unittest -b tests.store.AbstractCommonFileTestCase
    """

    def test_api_create(self) -> None:
        """test neutralisation de api_create"""
        s_err = "Impossible de créer un real_common_file."
        with self.assertRaises(StoreEntityError) as o_err:
            RealCommonFile.api_create(None)
        self.assertEqual(o_err.exception.message, s_err)

    def test_api_delete(self) -> None:
        """test neutralisation de api_delete"""
        s_err = "Impossible de supprimer un real_common_file."
        o_common = RealCommonFile({})
        with self.assertRaises(StoreEntityError) as o_err:
            o_common.api_delete()
        self.assertEqual(o_err.exception.message, s_err)
