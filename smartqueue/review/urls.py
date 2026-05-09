from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('all-reviews/', views.all_reviews, name='all_reviews'),
    path('my-reviews/', views.student_reviews, name='student_reviews'),
]
