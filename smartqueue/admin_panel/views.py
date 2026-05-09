from django.shortcuts import render, redirect
from datetime import date, timedelta
from queue_app.models import Queue


def admin_dashboard(request):

    tokens = Queue.objects.all()

    context = {
        'waiting_count': tokens.filter(status='waiting').count(),
        'current_serving': tokens.filter(status='serving').first(),
        'completed_count': tokens.filter(status='done').count(),
        'no_show_count': tokens.filter(status='no_show').count(),
        'all_tokens': tokens.order_by('-created_at')[:10]
    }
    return render(request, 'admin_panel/dashboard.html', context)


def call_next(request):

    current = Queue.objects.filter(status='serving').first()
    if current:
        current.status = 'done'
        current.save()


    next_token = Queue.objects.filter(status='waiting').order_by('created_at').first()
    if next_token:
        next_token.status = 'serving'
        next_token.save()

    return redirect('/admin-panel/')


def cancel_tomorrow(request):
    tomorrow = date.today() + timedelta(days=1)
    Queue.objects.filter(created_at__date=tomorrow).delete()
    return redirect('/admin-panel/')