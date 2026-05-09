from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg
from .models import Review


# ----------- SUBMIT REVIEW VIEW -----------
@require_POST
def submit_review(request):
    """Submit a review for a sector after queue completion"""
    student_id = request.POST.get('student_id')
    sector = request.POST.get('sector')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '')
    token_number = request.POST.get('token_number', '')

    if student_id and sector and rating:
        Review.objects.create(
            student_id=student_id,
            sector=sector,
            rating=int(rating),
            comment=comment,
            token_number=token_number
        )
        return JsonResponse({'success': True, 'message': 'Review submitted successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)


# ----------- VIEW ALL REVIEWS -----------
def all_reviews(request):
    """Display all reviews from all users"""
    reviews = Review.objects.all()
    
    # Sector-wise averages
    sectors = set(reviews.values_list('sector', flat=True))
    sector_stats = {}
    
    for sector in sectors:
        sector_reviews = reviews.filter(sector=sector)
        avg_rating = sector_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        count = sector_reviews.count()
        sector_stats[sector] = {
            'average': round(avg_rating, 2),
            'count': count
        }

    return render(request, 'all_reviews.html', {
        'reviews': reviews,
        'sector_stats': sector_stats,
    })


# ----------- STUDENT REVIEWS VIEW -----------
def student_reviews(request):
    """Display reviews submitted by the current student"""
    student_id = request.session.get('student_id')
    
    if not student_id:
        return redirect('student_login')
    
    reviews = Review.objects.filter(student_id=student_id).order_by('-created_at')
    
    return render(request, 'student_reviews.html', {
        'reviews': reviews,
        'student_id': student_id,
    })
