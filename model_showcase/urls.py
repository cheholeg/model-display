from django.urls import path

from model_showcase import views

app_name = "model_showcase"

urlpatterns = [
    path("", views.all_model_view, name="home"),
    path("search/", views.search_view, name="search"),
    path("info_model/", views.get_model_info, name="info_model"),
]
