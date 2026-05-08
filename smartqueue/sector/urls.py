from django.urls import path
from . import views

urlpatterns = [
    path("select/", views.select_sector, name="select_sector"),
]