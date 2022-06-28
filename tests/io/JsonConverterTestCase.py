import datetime
import json

from ignf_gpf_api.io.JsonConverter import JsonConverter
from tests.GpfTestCase import GpfTestCase


class JsonConverterTestCase(GpfTestCase):
    """Tests JsonConverterTestCase class.

    cmd : python3 -m unittest -b tests.io.JsonConverterTestCase
    """

    python_data = {
        "date": datetime.date(2020, 1, 1),
        "time": datetime.datetime(2020, 1, 1, 20, 0, 30).time(),
        "datetime": datetime.datetime(2020, 1, 1, 20, 0, 30),
    }
    json_data = {
        "date": "2020-01-01",
        "time": "20:00:30",
        "datetime": "2020-01-01T20:00:30",
    }

    def test_dumps(self) -> None:
        """Vérifie le bon fonctionnement de dumps."""
        o_json_converter = JsonConverter()
        s_text_data = o_json_converter.dumps(JsonConverterTestCase.python_data)
        self.assertEqual(json.dumps(JsonConverterTestCase.json_data), s_text_data)

    def test_convert(self) -> None:
        """Vérifie le bon fonctionnement de convert."""
        o_json_converter = JsonConverter()
        s_text_data = o_json_converter.convert(JsonConverterTestCase.python_data)
        self.assertDictEqual(JsonConverterTestCase.json_data, s_text_data)
