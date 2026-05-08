from django.shortcuts import render
from .models import QueueHistory


def student_history(request, student_id):

    history = QueueHistory.objects.filter(
        student_id=student_id
    ).order_by('-service_date')

    return render(request, 'student_history.html', {
        'history': history
    })