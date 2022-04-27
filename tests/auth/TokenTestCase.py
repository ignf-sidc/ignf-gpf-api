import unittest

from ignf_gpf_api.auth.Token import Token


class TokenTestCase(unittest.TestCase):
    """Tests ConfigTestCase class.

    cmd : python3 -m unittest -b ignf_gpf_api.tests.auth.TokenTestCase
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
        cToken = Token(TokenTestCase.valid_token)
        # On vérifie les données stockées
        self.assertEqual(cToken.get_access_string(), "test_token")

    def test_is_valid(self) -> None:
        """Vérifie le bon fonctionnement de is_valid."""
        # Création d'un token valide
        cToken = Token(TokenTestCase.valid_token)
        # On vérifie que c'est bien valide
        self.assertEqual(cToken.is_valid(), True)
        # Création d'un token non valide
        cToken = Token(TokenTestCase.invalid_token)
        # On vérifie que c'est bien non valide
        self.assertEqual(cToken.is_valid(), False)
