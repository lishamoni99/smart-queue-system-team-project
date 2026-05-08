from django.urls import path
from . import views

urlpatterns = [
    path("generate-token/", views.generate_token, name="generate_token"),
    path("queue-list/", views.queue_list, name="queue_list"),
    path("served/<int:id>/", views.mark_served, name="mark_served"),
    path("delete/<int:id>/", views.delete_token, name="delete_token"),
]