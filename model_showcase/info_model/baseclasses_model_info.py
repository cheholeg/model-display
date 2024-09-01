from typing import TYPE_CHECKING

from django.db.models import Model
from django.template.loader import render_to_string
from django.urls import reverse

from model_showcase.utils import get_model_path

if TYPE_CHECKING:
    from django.db.models.options import Options


class BaseClassesModelInfo:
    def __init__(
        self,
        model: type[Model],
    ):
        self._model = model
        self.model_name: str = self._get_base_model_name()
        self.model_path: str | None = self._get_base_model_path()
        self.url: str = self._get_url()

    def _get_base_model_name(self) -> str:
        return self._model.__name__

    def _get_base_model_path(self) -> str | None:
        opts: "Options[Model] | None" = getattr(self._model, "_meta", None)
        abstract: bool | None = opts.abstract if opts else None
        if not opts or abstract:
            return None
        return get_model_path(self._model)

    def _get_url(self) -> str:
        return reverse("model_showcase:info_model") + f"?model={ self.model_path }"


class ListBaseClassesModelInfo:
    template: str = "model_showcase/info_model/baseclasses.html"

    def __init__(
        self,
        model: type[Model],
    ):
        self._model = model
        self.base_models = self._get_baseclasses()

    def _get_baseclasses(self) -> list[BaseClassesModelInfo]:
        return [BaseClassesModelInfo(model) for model in self._model.__bases__]

    def render(self) -> str:
        context: dict[str, list[BaseClassesModelInfo]] = {"base_models": self.base_models}
        return render_to_string(self.template, context)
