from typing import TYPE_CHECKING

from django.test import TestCase

from test_lab.models import ModelTest
from model_showcase.info_model import InfoModel

if TYPE_CHECKING:
    from model_showcase.info_model.subclasses_model_info import SubClassesModelInfo


class TestModelInfo(TestCase):
    def setUp(self) -> None:  # type: ignore[explicit-override]
        self.model_info = InfoModel(ModelTest)  # type: ignore[misc]

    def test_base_field(self) -> None:
        self.assertEqual(self.model_info.model_name, "ModelTest")
        self.assertEqual(self.model_info.model_path, "test_lab.models.modeltest")
        self.assertEqual(self.model_info.verbose_name, "model test")
        self.assertEqual(self.model_info.db_table_name, "test_lab_modeltest")

    def test_base_model(self) -> None:
        self.assertEqual(len(self.model_info.baseclasses.base_models), 1)
        self.assertEqual(self.model_info.baseclasses.base_models[0].model_name, "BaseModelTest")
        self.assertEqual(
            self.model_info.baseclasses.base_models[0].model_path,
            "test_lab.models.basemodeltest",
        )

    def test_depth_subclasses_model_info(self) -> None:
        subclass: SubClassesModelInfo = self.model_info.subclasses
        empty_list: list[SubClassesModelInfo] = []
        self.assertNotEqual(subclass, empty_list)
        self.assertNotEqual(self.model_info.subclasses.subclasses, empty_list)
        self.assertEqual(self.model_info.subclasses.subclasses[1].subclasses, empty_list)
        self.assertNotEqual(self.model_info.subclasses.subclasses[0].subclasses, empty_list)
        self.assertEqual(
            self.model_info.subclasses.subclasses[0].subclasses[0].subclasses, empty_list
        )

    def test_related_model_info(self) -> None:
        self.assertEqual(len(self.model_info.related_model.related_models), 5)
        list_correct_model = [
            {
                "type": "ForeignKey",
                "possibles": [{"on_delete": "CASCADE"}],
                "name": "external_key",
                "verbose_name": "external key",
                "two_link": True,
            },
            {
                "type": "OneToOneField",
                "possibles": [{"on_delete": "PROTECT"}],
                "name": "external_key",
                "verbose_name": "external key",
                "two_link": True,
            },
            {
                "type": "ForeignKey",
                "possibles": [{"db_tablespace": ""}, {"on_delete": "CASCADE"}],
                "name": "modeltest",
                "verbose_name": "modeltest",
                "two_link": True,
            },
            {
                "type": "ManyToManyField",
                "possibles": [{"blank": True}],
                "name": "external_key",
                "verbose_name": "external key",
                "two_link": True,
            },
            {
                "type": "ForeignKey",
                "possibles": [{"on_delete": "PROTECT"}],
                "name": "external_key",
                "verbose_name": "external key",
                "two_link": False,
            },
        ]
        list_model = []
        for model_ in self.model_info.related_model.related_models:
            list_model += [
                {
                    "type": model_.get_field_type(),
                    "possibles": model_.get_possibles(),
                    "name": model_.get_field_name(),
                    "verbose_name": model_.get_field_verbose_name(),
                    "two_link": model_.two_way_link,
                },
            ]
        self.assertEqual(list_model, list_correct_model)
