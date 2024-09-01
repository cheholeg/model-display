import typing

from django.test import TestCase

from test_lab.models import ModelTest
from model_showcase.info_model import InfoModel

if typing.TYPE_CHECKING:
    from model_showcase.info_field.additional_info import EnumValue


class TestFieldInfo(TestCase):
    exclude_list: typing.ClassVar[list[str]] = ["_field", "_choices", "_tuple_enum", "enum_value"]

    def setUp(self) -> None:  # type: ignore[explicit-override]
        self.field_info = InfoModel(ModelTest).fields.fields  # type: ignore[misc]

    @staticmethod
    def get_dict_without_exclude_list(
        dict_field: dict[str, str | int | list[dict[str, str]]],
        exclude_list: list[str],
    ) -> dict[str, str | int | list[dict[str, str]]]:
        return {key: value for key, value in dict_field.items() if key not in exclude_list}

    def test_field_info(self) -> None:
        dict_base_field: dict[str, str | int | list[dict[str, str]]] = self.field_info[
            1
        ].__dict__
        dict_base_field = self.get_dict_without_exclude_list(dict_base_field, self.exclude_list)
        dict_with_correct_data = {
            "_db_table_name": "id",
            "_name": "id",
            "_possibles": [{"primary_key": True}, {"serialize": False}, {"auto_created": True}],
            "_type": "BigAutoField",
            "_verbose_name": "ID",
            "order": 2,
        }
        self.assertEqual(dict_base_field, dict_with_correct_data)

    def test_enum_value_info(self) -> None:
        enum_value: list[EnumValue] = getattr(self.field_info[2], "enum_value", [])
        self.assertEqual(len(enum_value), 2)
        dict_enum_value: dict[str, str | int | list[dict[str, str]]] = enum_value[
            0
        ].__dict__
        dict_enum_value = self.get_dict_without_exclude_list(dict_enum_value, self.exclude_list)
        dict_with_correct_data = {"caption": "Male", "value": "M"}
        self.assertEqual(dict_enum_value, dict_with_correct_data)

    def test_enum_field_info(self) -> None:
        dict_enum_field: dict[str, str | int | list[dict[str, str]]] = self.field_info[
            2
        ].__dict__
        dict_enum_field = self.get_dict_without_exclude_list(dict_enum_field, self.exclude_list)
        dict_with_correct_data = {
            "_db_table_name": "choices",
            "_name": "choices",
            "_possibles": [{"max_length": 3}],
            "_type": "CharField",
            "_verbose_name": "choices",
            "enum_field_model_name": "choices",
            "order": 2,
        }
        self.assertEqual(dict_enum_field, dict_with_correct_data)

    def test_link_field_info(self) -> None:
        dict_link_field: dict[str, str | int | list[dict[str, str]]] = self.field_info[
            0
        ].__dict__
        dict_link_field = self.get_dict_without_exclude_list(dict_link_field, self.exclude_list)
        dict_with_correct_data = {
            "_name": "basemodeltest_ptr",
            "_type": "OneToOneField",
            "_verbose_name": "basemodeltest ptr",
            "_db_table_name": "basemodeltest_ptr_id",
            "_possibles": [
                {"primary_key": True},
                {"serialize": False},
                {"auto_created": True},
                {"on_delete": "CASCADE"},
                {"parent_link": True},
            ],
            "order": 0,
            "model_name": "BaseModelTest",
            "verbose_name": "base model test",
            "model_path": "test_lab.models.basemodeltest",
            "two_way_link": True,
            "url": "/info_model/?model=test_lab.models.basemodeltest",
        }
        self.assertEqual(dict_link_field, dict_with_correct_data)
