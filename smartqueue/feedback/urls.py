from django.urls import path
from .views import create_feedback

urlpatterns = [
    path('', create_feedback, name='feedback_create'),
]