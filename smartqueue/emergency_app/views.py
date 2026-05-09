from django.shortcuts import render
from .models import EmergencyRequest

def emergency_dashboard(request):
    requests = EmergencyRequest.objects.all().order_by('-created_at')
    return render(request, 'emergency_app/emergency_list.html', {'requests': requests})
