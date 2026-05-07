
from django.shortcuts import render, redirect
from .models import Feedback

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get['student_name']
        rate = request.POST.get['rating']
        msg = request.POST.get['comment']

        Feedback.objects.create(
           student_name = name,
           rating = rate,
           comment = msg
        )
        return redirect('/')
    return render(request, 'feedback_form.html')

