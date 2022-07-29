from ignf_gpf_api.workflow.resolver.DictResolver import DictResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolverError

from tests.GpfTestCase import GpfTestCase


class DictResolverTestCase(GpfTestCase):
    """Tests DictResolver class.

    cmd : python3 -m unittest -b tests.workflow.resolver.DictResolverTestCase
    """

    def test_resolve(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve."""
        # Données
        d_data = {
            "titi": "toto",
            "tata": "tutu",
        }
        # Instanciation du résolveur
        o_resolver = DictResolver("4t", d_data)

        # test en mode réussite (avec toutes les clefs/valeurs de notre dict)
        for k, v in d_data.items():
            self.assertEqual(o_resolver.resolve(k), v)

        # test en mode erreur (exception levée + message ok)
        s_to_solve = "non_existant"
        with self.assertRaises(ResolverError) as o_arc:
            o_resolver.resolve(s_to_solve)
        self.assertEqual(o_arc.exception.message, f"Erreur du résolveur '4t' avec la chaîne '{s_to_solve}'.")
