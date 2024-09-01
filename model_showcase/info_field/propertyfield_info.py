from typing import TYPE_CHECKING

from django.db.models import Model
from django.template.loader import render_to_string

if TYPE_CHECKING:
    from collections.abc import Callable

class PropertyFieldInfo:
    """Базовый класс для создания property полей."""

    template: str = "model_showcase/info_field/property_field.html"

    def __init__(
        self,
        model: type[Model],
        property_field_name: str,
    ):
        self._model = model
        self.name: str = property_field_name
        self.type: str = self.get_property_type()
        self.verbose_name: str = self.get_property_verbose_name()

    def _get_property_field(self) -> property | None:
        property_: property | None = getattr(self._model, self.name, None)
        return property_

    def get_property_verbose_name(self) -> str:
        property_field = self._get_property_field()
        fget: Callable[[object], object] | None = getattr(property_field, "fget", None)
        if fget and callable(fget):
            verbose_name: str = getattr(fget, "short_description", "")
            return str(verbose_name) if verbose_name else ""
        return ""

    def get_property_type(self) -> str:
        property_field = self._get_property_field()
        fget: Callable[[object], object] | None = getattr(property_field, "fget", None)
        if fget and callable(fget):
            value_type: str | None = getattr(fget, "value_type", None)
            property_model: type[Model] | str | None = getattr(fget, "model", None)
            annotations: type | None = fget.__annotations__.get("return", None) if fget else None  # type: ignore[misc, truthy-function]
            type_field = value_type or property_model or annotations
            return str(type_field) if type_field else ""
        return ""

    def render(self) -> str:
        context: dict[str, PropertyFieldInfo] = {"field": self}
        return render_to_string(self.template, context)
