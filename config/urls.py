from django.urls import include, path
from routing import views

urlpatterns = [
    path("", views.map_page, name="home"),
    path("api/", include("routing.urls")),
]
