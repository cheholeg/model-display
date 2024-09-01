from django.test import TestCase

from test_lab.models import ModelTest
from model_showcase.info_model import InfoModel


class TestFieldInfo(TestCase):
    def setUp(self) -> None:  # type: ignore[explicit-override]
        self.property_info = InfoModel(ModelTest).property_fields.property_fields  # type: ignore[misc]

    def test_property_fields(self) -> None:
        list_field = []
        correct_property_fields = [
            {"name": "property_none", "type": "", "verbose_name": ""},
            {
                "name": "full_name",
                "type": "str | None",
                "verbose_name": "полное имя класса",
            },
        ]
        for field in self.property_info:
            dict_property_field: dict[str, object | str] = field.__dict__
            dict_property_field = {
                key: value for key, value in dict_property_field.items() if key not in ["_model"]
            }
            list_field += [dict_property_field]
        self.assertEqual(list_field, correct_property_fields)
