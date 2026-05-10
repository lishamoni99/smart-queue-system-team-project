from django.shortcuts import render, redirect
from .forms import FeedbackForm

def create_feedback(request):
    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')

    return render(request, 'feedback_form.html', {'form': form})