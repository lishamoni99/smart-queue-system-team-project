from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.feedback_view, name='feedback_form'),
]