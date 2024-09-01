from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Model
from django.template.loader import render_to_string

from model_showcase.info_field import RemoteField
from model_showcase.utils import ShowCollapseInModel

if TYPE_CHECKING:
    from django.contrib.contenttypes.fields import GenericForeignKey


class RelatedModelInfo:
    template: str = "model_showcase/info_model/related/related_model.html"

    def __init__(
        self,
        model: type[Model],
        show: ShowCollapseInModel | None = None,
    ):
        self._model = model
        self.related_models: list[RemoteField] = self._get_related_model()
        self._show = show

    def _get_related_model(self) -> list[RemoteField]:
        fields: (
            "list[models.Field[object, object] | models.ForeignObjectRel | GenericForeignKey]"
        )
        related_model_list = []
        link_to_yourself: str = "_ptr"
        fields = self._model._meta.get_fields(include_hidden=True)
        for field in fields:
            if isinstance(field, models.ForeignObjectRel) and field.remote_field:  # type: ignore[misc]
                remote_field_: "models.ForeignObject[object, object]" = field.remote_field
                if link_to_yourself in remote_field_.name:
                    continue
                remote_field = RemoteField(field)
                related_model_list += [remote_field]
        related_model_list.sort(key=lambda item: item.order)  # type: ignore[misc] # Any - item
        return related_model_list

    def render(self) -> str:
        show = bool(self._show == ShowCollapseInModel.RELATED)
        context: dict[str, list[RemoteField] | bool] = {
            "related_model_list": self.related_models,
            "show": show,
        }
        return render_to_string(
            self.template,
            context,
        )
