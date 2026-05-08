from django.urls import path
from . import views

urlpatterns = [

    path(
        'student-history/<int:student_id>/',
        views.student_history,
        name='student_history'
    ),

]