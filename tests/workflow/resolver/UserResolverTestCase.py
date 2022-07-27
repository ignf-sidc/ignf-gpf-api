from ignf_gpf_api.workflow.resolver.UserResolver import UserResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolveDataUsernameNotFound
from tests.GpfTestCase import GpfTestCase


class UserResolverTestCase(GpfTestCase):
    """Tests UserResolver class.

        cmd : python3 -m unittest -b tests.workflow.resolver.
    UserResolverTestCase
    """

    def test_can_solve_user(self) -> None:
        """test unitaire pour vérifier s'il réussit à récupérer les données de l'utilisateur authentifié"""

        s_name_resolver = "dpsg_resolver"
        s_to_solve_2 = "Phoebe"
        d_username_data = {
            "creation": "2022-05-08T15:02:10.095Z",
            "_id": "628b8b88001dae60e9fc2745",
            "communities_member": [
                {
                    "rights": {
                        "community_rights": "true",
                        "uploads_rights": "true",
                        "processings_rights": "true",
                        "datastore_rights": "true",
                        "stored_data_rights": "true",
                        "broadcast_rights": "true",
                    },
                    "community": {
                        "public": "false",
                        "_id": "6260157bf464ed789892bc04",
                        "name": "BAck office Géoplateforme",
                        "technical_name": "bag",
                        "supervisor": "6220b1ccd70753cdbe20351e",
                        "datastore": "626016c7f464ed698292bc42",
                    },
                }
            ],
            "email": "francois.bacquelot@ign.fr",
            "first_name": "François",
            "last_call": "2022-05-23T13:27:47.324Z",
            "last_name": "BACQUELOT",
        }

        # instanciation de l'objet lié à la classe UserResolver()
        o_resolver = UserResolver(s_name_resolver, d_username_data)

        # test en mode erreur
        with self.assertRaises(ResolveDataUsernameNotFound) as e_exception:
            o_resolver.resolve(s_to_solve_2)
        self.assertNotEqual(e_exception.exception.message, f"Le nom du username '{s_to_solve_2}' n'a pas pu récupéré les informations d'utilisateur lors de l'authentification.")
