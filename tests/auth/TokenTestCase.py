from ignf_gpf_api.auth.Token import Token
from tests.GpfTestCase import GpfTestCase


class TokenTestCase(GpfTestCase):
    """Tests Token class.

    cmd : python3 -m unittest -b tests.auth.TokenTestCase
    """

    valid_token = {
        "access_token": "test_token",
        "expires_in": 300,
    }
    invalid_token = {
        "access_token": "test_token",
        "expires_in": -300,
    }

    def test_get_access_string(self) -> None:
        """Vérifie le bon fonctionnement de get_access_string."""
        # Création d'un token
        o_token = Token(TokenTestCase.valid_token)
        # On vérifie les données stockées
        self.assertEqual(o_token.get_access_string(), "test_token")

    def test_is_valid(self) -> None:
        """Vérifie le bon fonctionnement de is_valid."""
        # Création d'un token valide
        o_token = Token(TokenTestCase.valid_token)
        # On vérifie que c'est bien valide
        self.assertEqual(o_token.is_valid(), True)
        # Création d'un token non valide
        o_token = Token(TokenTestCase.invalid_token)
        # On vérifie que c'est bien non valide
        self.assertEqual(o_token.is_valid(), False)
