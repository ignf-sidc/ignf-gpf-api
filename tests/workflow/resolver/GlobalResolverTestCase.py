from ignf_gpf_api.workflow.resolver.DictResolver import DictResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolverNotFoundError
from ignf_gpf_api.workflow.resolver.GlobalResolver import GlobalResolver

from tests.GpfTestCase import GpfTestCase


class GlobalResolverTestCase(GpfTestCase):
    """Tests GlobalResolver class.

    cmd : python3 -m unittest -b tests.workflow.resolver.GlobalResolverTestCase
    """

    localization = {
        "Jacques_country": "France",
        "Jacques_city": "Paris",
        "Jacques_street": "Champs-Elysée",
        "John_country": "England",
        "John_city": "London",
        "John_street": "rue_Londres",
    }
    profession = {
        "chef": "Jacques",
        "sailor": "John",
    }

    @classmethod
    def setUpClass(cls) -> None:
        """fonction lancée une fois avant tous les tests de la classe"""
        super().setUpClass()
        GlobalResolver().add_resolver(DictResolver("localization", GlobalResolverTestCase.localization))
        GlobalResolver().add_resolver(DictResolver("profession", GlobalResolverTestCase.profession))

    def test_add_resolver(self) -> None:
        """Vérifie le bon fonctionnement de la fonction add_resolver."""
        # La fonction a déjà été appelée dans le SetUpClass
        # On vérifie juste que l'on a bien 2 résolveurs
        self.assertEqual(len(GlobalResolver().resolvers), 2)
        self.assertTrue("localization" in GlobalResolver().resolvers)
        self.assertTrue("profession" in GlobalResolver().resolvers)

    def test_resolve(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve."""
        # Cas simples : une seule résolution
        self.assertEqual(GlobalResolver().resolve("{localization.Jacques_country}"), "France")
        self.assertEqual(GlobalResolver().resolve("{profession.sailor}"), "John")
        # Cas avancés : deux résolutions l'une dans l'autre
        self.assertEqual(GlobalResolver().resolve("{localization.{profession.sailor}_country}"), "England")
        self.assertEqual(GlobalResolver().resolve("{localization.{profession.chef}_city}"), "Paris")
        # Cas erreur :
        with self.assertRaises(ResolverNotFoundError) as o_arc:
            GlobalResolver().resolve("{resolver_not_found.foo}")
        self.assertEqual(o_arc.exception.resolver_name, "resolver_not_found")
        self.assertEqual(o_arc.exception.message, "Le résolveur 'resolver_not_found' demandé est non défini.")
