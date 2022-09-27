from django.urls import path

from . import views

app_name = "pipelines"
urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
]