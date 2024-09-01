from typing import TYPE_CHECKING

from django.db.models import Field, Model
from django.db.models.fields.related import RelatedField
from django.template.loader import render_to_string

from model_showcase.info_field import BaseFieldInfo, PropertyFieldInfo, LinkField, EnumField
from model_showcase.utils import ShowCollapseInModel

if TYPE_CHECKING:
    from django.utils.datastructures import ImmutableList


class FieldBuilder:
    """`create_field_info(self)` - информация о поле.

    Состоит из:
    base_field - основные поля
        или
    related_field - поля со связями
        или
    enum_field - поля с choice-ми
    """

    def __init__(
        self,
        field: "Field[object, object]",
    ):
        self._field = field

    def create_field_info(self) -> BaseFieldInfo:
        if isinstance(self._field, RelatedField):  # type: ignore[misc]
            return LinkField(self._field)
        choices: list[tuple[str, str]] = getattr(self._field, "choices", [])
        if choices:
            return EnumField(self._field)
        return BaseFieldInfo(self._field)


class ListFieldsModel:
    """Класс для сбора всех полей и их сортировки.

    1. Связанные поля имеющие двусторонние отношения.
    2. Оставшиеся связанные поля.
    3. Остальные поля.
    """

    template: str = "model_showcase/info_field/list_fields_model.html"

    def __init__(
        self,
        model: type[Model],
        show: ShowCollapseInModel | None = None,
    ):
        self._model = model
        self.fields: list[BaseFieldInfo] = self.get_fields()
        self._show = show

    def get_fields(self) -> list[BaseFieldInfo]:
        list_field: list[BaseFieldInfo] = []
        fields: "ImmutableList[Field[object, object]]" = self._model._meta.fields
        for field in fields:
            field_info_builder = FieldBuilder(field)
            field_info: BaseFieldInfo = field_info_builder.create_field_info()
            list_field.append(field_info)
        list_field.sort(key=lambda item: item.order)  # type: ignore[misc] # Any - item
        return list_field

    def render(self) -> str:
        show: bool = bool(not self._show or self._show == ShowCollapseInModel.FIELD)
        context: dict[str, list[BaseFieldInfo] | bool] = {"fields": self.fields, "show": show}
        return render_to_string(self.template, context)


class ListPropertyFieldsModel:
    """Класс для сбора всех property полей."""

    template: str = "model_showcase/info_field/list_property_fields.html"

    def __init__(
        self,
        model: type[Model],
        show: ShowCollapseInModel | None = None,
    ):
        self._model = model
        self.property_fields: list[PropertyFieldInfo] = self.get_property_fields()
        self._show = show

    def get_property_fields(self) -> list[PropertyFieldInfo]:
        property_fields = []
        for property_field_name in vars(self._model):  # type: ignore[misc]
            if isinstance(getattr(self._model, property_field_name), property):  # type: ignore[misc]
                field_property = PropertyFieldInfo(self._model, property_field_name)
                property_fields.append(field_property)
        return property_fields

    def render(self) -> str:
        show = bool(self._show == ShowCollapseInModel.PROPERTY)
        context: dict[str, list[PropertyFieldInfo] | bool] = {
            "property_fields": self.property_fields,
            "show": show,
        }
        return render_to_string(self.template, context)
