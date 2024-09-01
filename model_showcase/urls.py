from django.urls import path, reverse_lazy

from model_showcase import views
from django.contrib.auth import views as auth_views

app_name = "model_showcase"

urlpatterns = [
    path("", views.all_model_view, name="home"),
    path("search/", views.search_view, name="search"),
    path("info_model/", views.get_model_info, name="info_model"),
    path("login/", auth_views.LoginView.as_view(next_page=reverse_lazy("model_showcase:home")), name="login"),  # type: ignore[misc]
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("model_showcase:home")), name="logout"),  # type: ignore[misc]
]
