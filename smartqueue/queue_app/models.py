from django.db import models
from accounts.models import Student

class Queue(models.Model):
    SECTOR_CHOICES = [
        ('Bank', 'Bank'),
        ('Library', 'Library'),
        ('Office', 'Office'),
        ('Canteen', 'Canteen'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)

    token = models.CharField(max_length=10)
    position = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="waiting")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token