from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(next_page="/"), name="login"),  # type: ignore[misc]
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),  # type: ignore[misc]
    path("", include("model_showcase.urls", namespace="model_showcase")),
]
