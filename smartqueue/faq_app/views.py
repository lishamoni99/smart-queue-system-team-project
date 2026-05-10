from django.shortcuts import render
from .models import FAQ

def faq_list(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'faq_app/faq.html', {'faqs': faqs})