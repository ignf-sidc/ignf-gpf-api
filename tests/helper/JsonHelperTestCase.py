from pathlib import Path

from ignf_gpf_api.helper.JsonHelper import JsonHelper
from ignf_gpf_api.Errors import GpfApiError
from tests.GpfTestCase import GpfTestCase


class JsonHelperTestCase(GpfTestCase):
    """Test de la classe JsonHelper : on doit pouvoir ouvrir des JSON avec des commentaires !
    Et on doit pouvoir valider des schéma JSON avec des messages précis selon l'erreur.

    cmd : python3 -m unittest -b tests.helper.JsonHelperTestCase
    """

    data_path = GpfTestCase.test_dir_path / "helper" / "JsonHelper"

    def test_load(self) -> None:
        """load ok quand le fichier existe, n'existe pas / n'est pas valide (et quant on veut un message personnalisé)."""
        # Non existant : Propriétés
        p_json_path = Path("/not/existing/file")

        # Non existant : Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.load(p_json_path)
        # Vérification du message renvoyé
        s_message = f"Fichier JSON {p_json_path} non trouvé"
        self.assertIn(s_message, o_arc.exception.message)

        # Non existant : Une exception levée avec un message personnalisé
        s_pattern = "Fichier {json_path} non trouvé, cela est vraiment dommage..."
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.load(p_json_path, file_not_found_pattern=s_pattern)
        # Vérification du message renvoyé
        s_message = s_pattern.format(json_path=p_json_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # Non parsable : Propriétés
        p_json_path = JsonHelperTestCase.data_path / "json_not_parsable.json"

        # Non parsable : Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.load(p_json_path)
        # Vérification du message renvoyé
        s_message = f"Fichier JSON {p_json_path} non parsable"
        self.assertIn(s_message, o_arc.exception.message)

        # Non parsable : Une exception levée avec un message personnalisé
        s_pattern = "Fichier JSON {json_path} non parsable, cela est vraiment dommage..."
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.load(p_json_path, file_not_parsable_pattern=s_pattern)
        # Vérification du message renvoyé
        s_message = s_pattern.format(json_path=p_json_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # Parsable : Propriétés
        p_json_path = JsonHelperTestCase.data_path / "json_parsable.json"

        # Parsable
        d_data = JsonHelper.load(p_json_path)
        # Vérification du contenu lu
        self.assertEqual(d_data["name"], "json parsable")
        self.assertEqual(d_data["title"], "il y a une virgule !")

    def test_loads(self) -> None:
        """loads ok quand la string est valide / n'est pas valide (et quant on veut un message personnalisé)."""
        # Non parsable : Propriétés
        s_data = '{"name": "key" "title": "pas de virgule"}'
        s_title = "non valide"
        s_error = "Expecting ',' delimiter: line 1 column 16 (char 15)"

        # Non parsable : Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.loads(s_data, s_title)
        # Vérification du message renvoyé
        s_start = f"Impossible de parser le JSON «{s_title}»"
        self.assertIn(s_start, o_arc.exception.message)
        self.assertIn(s_error, o_arc.exception.message)

        # Non parsable : Une exception levée avec un message personnalisé
        s_pattern = "Données {title} non parsable, cela est vraiment dommage..."
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.loads(s_data, s_title, message_pattern=s_pattern)
        # Vérification du message renvoyé
        s_message = s_pattern.format(title=s_title)
        self.assertEqual(s_message, o_arc.exception.message)

        # Parsable : Propriétés
        s_data = '{"name": "json parsable", "title": "il y a une virgule !"}'

        # Parsable
        d_data = JsonHelper.loads(s_data, "valide")
        # Vérification du contenu lu
        self.assertEqual(d_data["name"], "json parsable")
        self.assertEqual(d_data["title"], "il y a une virgule !")

    def test_validate_dict(self) -> None:
        """validate_dict ok quand c'est valide / pas valide (json ou schéma)."""
        # Propriétés générales
        s_json_not_valid = "le json n'est pas valide"
        s_schema_not_valid = "le schéma n'est pas valide"

        # Schéma non valide : Propriétés
        p_schema_invalid_path = JsonHelperTestCase.data_path / "json_not_valid.json"
        d_schema_invalid_data = JsonHelper.load(p_schema_invalid_path)
        d_json_data = {"name": "toto", "title": "titi"}
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_object(d_json_data, d_schema_invalid_data, s_json_not_valid, s_schema_not_valid)
        # Vérification du message renvoyé
        self.assertEqual(s_schema_not_valid, o_arc.exception.message)

        # JSON non valide : Propriétés
        p_schema_path = JsonHelperTestCase.data_path / "schema.json"
        d_schema_data = JsonHelper.load(p_schema_path)
        d_json_data = {"tutu": "toto", "tata": "titi"}
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_object(d_json_data, d_schema_data, s_json_not_valid, s_schema_not_valid)
        # Vérification du message renvoyé
        self.assertEqual(s_json_not_valid, o_arc.exception.message)

        # JSON valide : Propriétés
        p_schema_path = JsonHelperTestCase.data_path / "schema.json"
        d_schema_data = JsonHelper.load(p_schema_path)
        d_json_data = {"name": "toto", "title": "titi"}
        # Ca passe
        JsonHelper.validate_object(d_json_data, d_schema_data, s_json_not_valid, s_schema_not_valid)

    def test_validate_json(self) -> None:
        """validate_dict ok quand c'est valide / pas valide (json ou schéma)."""
        # Propriétés générales
        # Chemins vers les différents fichiers
        p_invalid_schema_path = JsonHelperTestCase.data_path / "json_not_valid.json"
        p_valid_schema_path = JsonHelperTestCase.data_path / "schema.json"
        p_invalid_json_path = JsonHelperTestCase.data_path / "json_not_valid.json"
        p_valid_json_path = JsonHelperTestCase.data_path / "json_parsable.json"
        p_not_parsable_path = JsonHelperTestCase.data_path / "json_not_parsable.json"
        # Pattern de base des messages
        s_schema_not_found_pattern = "Le schéma JSON {schema_path} n'existe pas. Contactez le support."
        s_schema_not_parsable_pattern = "Le schéma JSON {schema_path} n'est pas parsable. Contactez le support."
        s_schema_not_valid_pattern = "Le schéma JSON {schema_path} n'est pas valide. Contactez le support."
        s_json_not_found_pattern = "Le fichier JSON {json_path} n'existe pas. Contactez le support."
        s_json_not_parsable_pattern = "Le fichier JSON {json_path} n'est pas parsable. Contactez le support."
        s_json_not_valid_pattern = "Le fichier JSON {json_path} n'est pas valide. Contactez le support."

        # Schéma non trouvé
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(p_valid_json_path, Path("/not/found"))
        # Vérification du message renvoyé
        s_message = s_schema_not_found_pattern.format(schema_path=Path("/not/found"))
        self.assertEqual(s_message, o_arc.exception.message)

        # JSON non trouvé
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(Path("/not/found"), p_valid_schema_path)
        # Vérification du message renvoyé
        s_message = s_json_not_found_pattern.format(json_path=Path("/not/found"))
        self.assertEqual(s_message, o_arc.exception.message)

        # Schéma non parsable
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(p_valid_json_path, p_not_parsable_path)
        # Vérification du message renvoyé
        s_message = s_schema_not_parsable_pattern.format(schema_path=p_not_parsable_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # JSON non parsable
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(p_not_parsable_path, p_valid_schema_path)
        # Vérification du message renvoyé
        s_message = s_json_not_parsable_pattern.format(json_path=p_not_parsable_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # Schéma non valide
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(p_valid_json_path, p_invalid_schema_path)
        # Vérification du message renvoyé
        s_message = s_schema_not_valid_pattern.format(schema_path=p_invalid_schema_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # JSON non valide
        # Une exception levée avec le message de base
        with self.assertRaises(GpfApiError) as o_arc:
            JsonHelper.validate_json(p_invalid_json_path, p_valid_schema_path)
        # Vérification du message renvoyé
        s_message = s_json_not_valid_pattern.format(json_path=p_invalid_json_path)
        self.assertEqual(s_message, o_arc.exception.message)

        # JSON et schéma valide - Ca passe
        JsonHelper.validate_json(p_valid_json_path, p_valid_schema_path)
