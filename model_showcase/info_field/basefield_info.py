from typing import ClassVar, TYPE_CHECKING, ParamSpec

if TYPE_CHECKING:
    from django.db.models import Field
    from collections.abc import Callable, Sequence
from django.template.loader import render_to_string

from model_showcase.utils import ContextualClasses, Order

P = ParamSpec("P")


class BaseFieldInfo:
    """Базовый класс для создания полей."""

    template: str = "model_showcase/info_field/base_field.html"
    contextual_classes = ContextualClasses.LIGHT
    already_used_possibles: ClassVar[list[str]] = ["verbose_name", "to", "choices"]

    def __init__(
        self,
        field: "Field[object, object]",
    ):
        self._field = field
        self._name: str | None = self.get_field_name()
        self._type: str = self.get_field_type()
        self._verbose_name: str | None = self.get_field_verbose_name()
        self._db_table_name: str | None = self.get_db_table_name()
        self._possibles: list[dict[str, str]] = self.get_possibles()
        self.order: int = Order.LAST

    def get_field_name(self) -> str | None:
        name: str | None = getattr(self._field, "name", None)
        return name

    def get_field_type(self) -> str:
        deconstruct: tuple[str, str, Sequence[str], dict[str, str | Callable[P, None]]] = (
            self._field.deconstruct()
        )
        field_path: str = deconstruct[1]
        field_type = field_path.split(".")[-1]
        return field_type  # noqa: RET504

    def get_field_verbose_name(self) -> str | None:
        verbose_name: str | None = getattr(self._field, "verbose_name", None)
        return verbose_name

    def get_possibles(self) -> list[dict[str, str]]:
        list_possibles = []
        deconstruct: tuple[str, str, Sequence[str], dict[str, str | Callable[P, None]]] = (
            self._field.deconstruct()
        )
        kwargs: dict[str, (str | Callable[P, None])] = deconstruct[3]
        for possible in kwargs:
            dict_possibles: dict[str, str] = {}
            if callable(kwargs[possible]):
                try:
                    dict_possibles[possible] = kwargs[possible].__name__  # type: ignore[union-attr, misc]
                except AttributeError:
                    dict_possibles[possible] = "Невозможно вывести имя функции"
            elif possible not in self.already_used_possibles:
                dict_possibles[possible] = kwargs[possible]  # type: ignore[assignment]
            if dict_possibles:
                list_possibles.append(dict_possibles)
        return list_possibles

    def render(self) -> str:
        context: dict[str, BaseFieldInfo] = {"field": self}
        return render_to_string(self.template, context)

    def get_db_table_name(self) -> str | None:
        column: str | None = getattr(self._field, "column", None)
        return column

    def get_contextual_classes(self) -> str:
        return self.contextual_classes
