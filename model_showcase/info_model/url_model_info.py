from typing import override

from django.contrib import admin
from django.db.models import Model
from django.template.loader import render_to_string
from django.urls import reverse


class ModelLinksHandler:
    msg = "Метод должен быть переопределен в наследнике"

    def __init__(self, model: type[Model]) -> None:
        self._model: type[Model] = model
        self.name: str | None = self._get_name()
        self.link: str | None = self._get_link()

    def _get_name(self) -> str | None:
        raise NotImplementedError(self.msg)

    def _get_link(self) -> str | None:
        raise NotImplementedError(self.msg)

    def value_is_not_none(self) -> bool:
        return all([self.name and self.link])


class ModelLinks:
    template = "model_showcase/info_model/links.html"

    def __init__(self, model: type[Model]) -> None:
        self._links: list[ModelLinksHandler] = self._get_list_links(model)

    def _get_list_links(self, model: type[Model]) -> list[ModelLinksHandler]:
        list_links = []
        subclasses = ModelLinksHandler.__subclasses__()
        for subclass in subclasses:
            model_link = subclass(model)
            if model_link.value_is_not_none():
                list_links.append(model_link)
        return list_links

    def render(self) -> str:
        context: dict[str, list[ModelLinksHandler]] = {"urls": self._links}
        return render_to_string(
            self.template,
            context,
        )


class AdminModelLinks(ModelLinksHandler):
    viewname = "changelist"

    @override
    def _get_name(self) -> str | None:
        if admin.site.is_registered(self._model):
            return "Админка: список объектов"
        return None

    @override
    def _get_link(self) -> str | None:
        if admin.site.is_registered(self._model):
            url_viewname = (
                f"{self._model._meta.app_label}_{self._model._meta.model_name}_{self.viewname}"
            )
            url_with_admin_namespace = "admin:" + url_viewname
            return reverse(url_with_admin_namespace)
        return None
