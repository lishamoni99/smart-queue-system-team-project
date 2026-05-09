from django.shortcuts import render
from .models import Notification


def inbox(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return render(request, 'inbox.html', {'error': 'Session expired. Please login again.'})


    notifications = Notification.objects.filter(student_id=student_id).order_by('-created_at')

    Notification.objects.filter(student_id=student_id, is_read=False).update(is_read=True)

    return render(request, 'inbox.html', {
        'notifications': notifications
    })