from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.workflow.resolver.UserResolver import UserResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolveUserError

from tests.GpfTestCase import GpfTestCase


class UserResolverTestCase(GpfTestCase):
    """Tests UserResolver class.

    cmd : python3 -m unittest -b tests.workflow.resolver.UserResolverTestCase
    """

    def test_can_solve_user(self) -> None:
        """test unitaire pour vérifier s'il réussit à récupérer les données de l'utilisateur"""

        # Données de l’utilisateur
        d_user_data = {
            "creation": "2022-05-08T15:02:10.095Z",
            "_id": "628b8b88001dae60e9fc2745",
            "email": "prenom.nom@ign.fr",
            "first_name": "First Name",
            "last_call": "2022-05-23T13:27:47.324Z",
            "last_name": "Last Name",
        }
        # Création d'une fausse réponse contenant les données utilisateurs renvoyées par l'API
        o_response = GpfTestCase.get_response(json=d_user_data)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # instanciation de l'objet lié à la classe UserResolver()
            o_resolver = UserResolver("user")
            # La fonction route_request a déjà dû être appelée 1 fois
            o_mock_request.assert_called_once_with("user_get")

        # test en mode réussite (avec toutes les clefs/valeurs de notre dict)
        for k, v in d_user_data.items():
            self.assertEqual(o_resolver.resolve(k), v)

        # test en mode erreur (exception levée + message ok)
        s_to_solve = "non_existant"
        with self.assertRaises(ResolveUserError) as e_exception:
            o_resolver.resolve(s_to_solve)
        self.assertEqual(e_exception.exception.message, f"Erreur de récupération des données de l'utilisateur (résolveur 'user') avec la chaîne '{s_to_solve}'.")

        # La fonction doit toujours n'avoir été appelée qu'une fois
        o_mock_request.assert_called_once_with("user_get")
