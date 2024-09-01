from typing import ClassVar, override

from django.apps import apps
from django.db import models
from django.db.models import Field, OneToOneField, ManyToManyField, ForeignObjectRel
from django.template.loader import render_to_string
from django.urls import reverse

from model_showcase.info_field import BaseFieldInfo
from model_showcase.utils import get_model_path, ContextualClasses, Order


class LinkField(BaseFieldInfo):
    """Класс для создания полей со связями."""

    template: str = "model_showcase/info_field/additional_fields/link_field.html"
    contextual_classes: str = ContextualClasses.INFO

    def __init__(
        self,
        field: "Field[object, object]",
    ):
        super().__init__(field)
        self.model_name: str = self._get_related_model_name()
        self.verbose_name: str = self._get_related_verbose_name()
        self.model_path: str = self._get_related_model_path()
        self.two_way_link: bool = self._get_two_way_link()
        self.order: int = self._get_order()
        self.url: str = self._get_url()

    def _get_related_model_name(self) -> str:
        related_model: type | str | None = self._field.related_model
        if isinstance(related_model, str):
            related_model = apps.get_model(self._field.model._meta.app_label, related_model)
        if related_model is not None:
            name: str = related_model.__name__
            return name
        return ""

    def _get_related_verbose_name(self) -> str:
        related_model: type | str | None = self._field.related_model
        if isinstance(related_model, type) and issubclass(related_model, models.Model):  # type: ignore[misc] # any
            verbose_name: str = getattr(related_model._meta, "verbose_name", "")
            return verbose_name
        return ""

    def _get_related_model_path(self) -> str:
        related_model: type | str | None = self._field.related_model
        if isinstance(related_model, type):  # type: ignore[misc] # any
            return get_model_path(related_model)
        return ""

    def _get_two_way_link(self) -> bool:
        return self._check_by_two_way_link()

    def _get_order(self) -> int:
        if self.two_way_link:
            return Order.FIRST
        return Order.CENTER

    def _check_by_two_way_link(self) -> bool:
        if isinstance(self._field, OneToOneField | ManyToManyField) or (  # type: ignore[misc] # any
            getattr(self._field.remote_field, "on_delete", None) is models.CASCADE  # type: ignore[misc] # any
        ):
            return True
        return False

    @override
    def get_contextual_classes(self) -> str:
        if self._get_two_way_link():
            return ContextualClasses.PRIMARY
        return self.contextual_classes

    @override
    def render(self) -> str:
        context: dict[str, LinkField] = {"field": self}
        return render_to_string(self.template, context)

    def _get_url(self) -> str:
        return reverse("model_showcase:info_model") + f"?model={self.model_path}"


class RemoteField(LinkField):
    template: str = "model_showcase/info_field/additional_fields/remote_field.html"
    already_used_possibles: ClassVar[list[str]] = ["related_name", "verbose_name", "to", "choices"]

    def __init__(
        self,
        field: ForeignObjectRel,
    ):
        self._remote_field = field
        remote_field: "models.ForeignObject[object, object]" = field.remote_field
        super().__init__(remote_field)

    @override
    def _get_related_model_name(self) -> str:
        related_model = self._remote_field.related_model
        if isinstance(related_model, type):  # type: ignore[misc] # any
            return related_model.__name__
        return ""

    @override
    def _get_related_verbose_name(self) -> str:
        related_model = self._remote_field.related_model = self._remote_field.related_model
        if isinstance(related_model, type) and hasattr(related_model, "_meta"):  # type: ignore[misc] # any
            verbose_name = related_model._meta.verbose_name
            return str(verbose_name) or ""
        return ""

    @override
    def _get_related_model_path(self) -> str:
        related_model = self._remote_field.related_model
        if isinstance(related_model, type):  # type: ignore[misc] # any
            return get_model_path(related_model)
        return ""

    def get_related_name(self) -> str:
        related_name = self._remote_field.related_name
        if not related_name:
            return "Параметр не задан"
        if self._remote_field.hidden:
            return "Обратная связь не создана"
        return related_name

    @override
    def render(self) -> str:
        context: dict[str, RemoteField] = {"field": self}
        return render_to_string(self.template, context)


class EnumValue:
    template = "model_showcase/info_field/additional_fields/enum/enum_value.html"

    def __init__(
        self,
        choices: list[tuple[str, str]],
        tuple_enum: tuple[str, str],
    ):
        self._choices = choices
        self._tuple_enum = tuple_enum
        self.value = tuple_enum[0]
        self.caption = tuple_enum[1]

    def render(self) -> str:
        context: dict[str, EnumValue] = {"enum": self}
        return render_to_string(self.template, context)


class EnumField(BaseFieldInfo):
    """Класс для создания полей с choice-ми."""

    template = "model_showcase/info_field/additional_fields/enum/enum_field.html"

    def __init__(
        self,
        field: "Field[object, object]",
    ):
        super().__init__(field)
        self.enum_value: list[EnumValue] = self._get_value_enum()
        self.enum_field_model_name: str = self._get_enum_field_model_name()

    def _get_value_enum(self) -> list[EnumValue]:
        choises: list[tuple[str, str]] = getattr(self._field, "choices", [])
        enum_value: list[EnumValue] = [EnumValue(choises, choice) for choice in choises]
        return enum_value

    def _get_enum_field_model_name(self) -> str:
        name: str = getattr(self._field, "verbose_name", "")
        return name

    @override
    def render(self) -> str:
        context: dict[str, EnumField] = {"field": self}
        return render_to_string(self.template, context)

    @override
    def get_contextual_classes(self) -> str:
        return self.contextual_classes
