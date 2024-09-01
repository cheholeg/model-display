from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from model_showcase.serializers import (
    find_all_model_list,
    find_model_list_by_search_word,
    get_model_info_by_model_path,
)
from model_showcase.utils import ShowCollapseInModel

if TYPE_CHECKING:
    from model_showcase.info_model import InfoModel


@login_required(login_url="model_showcase:login")  # type: ignore[misc]
def all_model_view(request: WSGIRequest) -> HttpResponse:
    context = find_all_model_list()
    return render(request, "model_showcase/index.html", context)


@login_required(login_url="model_showcase:login")  # type: ignore[misc]
def search_view(request: WSGIRequest) -> HttpResponse:
    query = request.GET.get("query")
    context = find_model_list_by_search_word(query) if query else None
    return render(request, "model_showcase/search.html", context)


@login_required(login_url="model_showcase:login")  # type: ignore[misc]
def get_model_info(request: WSGIRequest) -> HttpResponse:
    model_path = request.GET.get("model")
    show_value = request.GET.get("show")
    show = ShowCollapseInModel(show_value) if show_value else None
    info_model = get_model_info_by_model_path(model_path, show) if model_path else None
    context: dict[str, InfoModel | ShowCollapseInModel | None] = {
        "model": info_model,
        "show": show,
    }
    return render(request, "model_showcase/info_model/model_info.html", context)
