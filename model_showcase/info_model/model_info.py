from typing import TypedDict

from django.db.models import Model
from django.urls import reverse

from model_showcase.info_field import PropertyFieldInfo, RemoteField
from model_showcase.info_field.builder import ListFieldsModel, ListPropertyFieldsModel
from model_showcase.info_model.baseclasses_model_info import ListBaseClassesModelInfo
from model_showcase.info_model.related_model_info import RelatedModelInfo
from model_showcase.info_model.subclasses_model_info import SubClassesModelInfo
from model_showcase.info_model.url_model_info import ModelLinks
from model_showcase.utils import get_model_path, ShowCollapseInModel


class ShowUrl(TypedDict):
    name: str
    url: str


class InfoModel:
    def __init__(
        self,
        model: type[Model],
        show: ShowCollapseInModel | None = None,
    ):
        self._model = model
        self.model_name: str | None = self._get_model_name()
        self.model_path: str | None = self._get_model_path()
        self.verbose_name: str | None = self._get_verbose_name()
        self.db_table_name: str | None = self._get_table()
        self.subclasses: SubClassesModelInfo = SubClassesModelInfo(self._model)
        self.baseclasses: ListBaseClassesModelInfo = ListBaseClassesModelInfo(self._model)
        self.related_model: RelatedModelInfo = RelatedModelInfo(self._model, show=show)
        self.fields: ListFieldsModel = ListFieldsModel(self._model, show=show)
        self.property_fields: ListPropertyFieldsModel = ListPropertyFieldsModel(
            self._model, show=show
        )
        self.url: str = self._get_url()
        self.another_link: list[ShowUrl] = self._get_another_link()
        self.links: ModelLinks = ModelLinks(self._model)

    def _get_model_name(self) -> str:
        return self._model.__name__

    def _get_verbose_name(self) -> str:
        verbose_name: str = getattr(self._model._meta, "verbose_name", "")
        return verbose_name

    def _get_table(self) -> str:
        return self._model._meta.db_table

    def _get_model_path(self) -> str | None:
        return get_model_path(self._model) if self._model else None

    def get_property_fields(self) -> list[PropertyFieldInfo]:
        return self.property_fields.property_fields

    def get_subclasses(self) -> list[SubClassesModelInfo]:
        return self.subclasses.subclasses

    def get_related_model(self) -> list[RemoteField]:
        return self.related_model.related_models

    def _get_url(self) -> str:
        return reverse("model_showcase:info_model") + f"?model={self.model_path}"

    def _get_show_model_property_field(self) -> ShowUrl | None:
        if self.get_property_fields():
            return {
                "name": "Property поля",
                "url": self.url + f"&show={ShowCollapseInModel.PROPERTY.value}",
            }
        return None

    def _get_show_model_subclass(self) -> ShowUrl | None:
        if self.get_subclasses():
            return {
                "name": "Наследники",
                "url": self.url + f"&show={ShowCollapseInModel.SUBCLASS.value}",
            }
        return None

    def _get_show_related_model(self) -> ShowUrl | None:
        if self.get_related_model():
            return {
                "name": "Связанные модели",
                "url": self.url + f"&show={ShowCollapseInModel.RELATED.value}",
            }
        return None

    def _get_another_link(self) -> list[ShowUrl]:
        return [
            link
            for get_link in (
                self._get_show_model_property_field,
                self._get_show_model_subclass,
                self._get_show_related_model,
            )
            if (link := get_link())
        ]
