from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'sector', 'rating', 'created_at')
    list_filter = ('sector', 'rating', 'created_at')
    search_fields = ('student_id', 'sector', 'comment')
    readonly_fields = ('created_at',)
