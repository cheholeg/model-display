from django.db.models import Model
from django.urls import reverse

from model_showcase.utils import get_model_path


class SubClassesModelInfo:
    def __init__(
        self,
        model: type[Model],
    ):
        self._model = model
        self.model_name: str = self._get_sub_model_name()
        self.verbose_name: str = self._get_sub_verbose_name()
        self.model_path: str = self._get_sub_model_path()
        self.url: str = self._get_url()
        self.subclasses: list[SubClassesModelInfo] = self._get_subclasses()

    def _get_sub_model_name(self) -> str:
        return self._model.__name__

    def _get_sub_verbose_name(self) -> str:
        verbose_name: str = getattr(self._model._meta, "verbose_name", "")
        return verbose_name

    def _get_sub_model_path(self) -> str:
        return get_model_path(self._model)

    def _get_subclasses(self) -> list["SubClassesModelInfo"]:
        return [SubClassesModelInfo(model) for model in self._model.__subclasses__()]

    def _get_url(self) -> str:
        return reverse("model_showcase:info_model") + f"?model={ self.model_path }"
