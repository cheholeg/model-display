from enum import Enum

from django.db.models import Model


class ContextualClasses(str):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


class Order(int):
    FIRST = 0
    CENTER = 1
    LAST = 2


class ShowCollapseInModel(str, Enum):
    FIELD = "field"
    PROPERTY = "property"
    SUBCLASS = "subclass"
    RELATED = "related"


def get_model_path(model: type[Model]) -> str:
    return (model.__module__ + "." + model.__name__).lower()


def _get_model_set(search_word: str, model: type[Model]) -> set[type[Model]]:
    search_word = search_word.lower()
    set_models = set()
    for model_ in model.__subclasses__():
        if search_word == get_model_path(model_):
            set_models.add(model_)
        verbose_name: str = getattr(model_._meta, "verbose_name", "")
        verbose_name_plural: str = getattr(model_._meta, "verbose_name_plural", "")
        if (
            search_word in model_.__name__.lower()
            or (verbose_name and search_word in verbose_name.lower())
            or (verbose_name_plural is not None and search_word in verbose_name_plural.lower())
        ) and not model_._meta.abstract:
            set_models.add(model_)
        set_models |= _get_model_set(search_word, model_)
    return set_models


def _get_all_model_set(model: type[Model]) -> set[type[Model]]:
    set_models = set()
    for model_ in model.__subclasses__():
        if not model_._meta.abstract:
            set_models.add(model_)
        set_models |= _get_all_model_set(model_)
    return set_models


def get_all_model_set() -> list[type[Model]]:
    return list(_get_all_model_set(Model))  # type: ignore[misc]


def get_model_set_by_search_word(search_word: str) -> list[type[Model]]:
    return list(_get_model_set(search_word, Model))  # type: ignore[misc]


def get_model_set_by_model_path(model_path: str) -> type[Model]:
    model_list = list(_get_model_set(model_path, Model))  # type: ignore[misc]
    return [model for model in model_list if get_model_path(model) == model_path][0]
