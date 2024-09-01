from django.db.models import Model

from model_showcase.info_model import InfoModel
from model_showcase.utils import (
    get_all_model_set,
    get_model_set_by_model_path,
    get_model_set_by_search_word,
    ShowCollapseInModel,
)


def _get_dict_model_by_model_list(model_list: list[type[Model]]) -> list[InfoModel]:
    list_models = []
    model_list.sort(key=lambda item: item.__name__)  # type: ignore[misc] # Any - item
    for model in model_list:
        model_info = InfoModel(model=model)
        list_models += [model_info]
    return list_models


def find_model_list_by_search_word(search_word: str) -> dict[str, str | list[InfoModel]]:
    model_list = get_model_set_by_search_word(search_word)
    list_models = _get_dict_model_by_model_list(model_list)
    return {
        "query": search_word,
        "results": list_models,
    }


def find_all_model_list() -> dict[str, list[InfoModel]]:
    model_list = get_all_model_set()
    list_models = _get_dict_model_by_model_list(model_list)
    return {
        "model_list": list_models,
    }


def get_model_info_by_model_path(model_path: str, show: ShowCollapseInModel | None) -> InfoModel:
    model = get_model_set_by_model_path(model_path)
    return InfoModel(model, show)
