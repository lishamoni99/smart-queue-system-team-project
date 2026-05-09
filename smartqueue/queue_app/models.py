from django.db import models


# ---------------- STUDENT MODEL ----------------
from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default="Student")

    image = models.ImageField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return self.student_id


# ---------------- GUARDIAN MODEL ----------------
class Guardian(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, default="Guardian")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.phone


# ---------------- QUEUE / TOKEN MODEL (VERY IMPORTANT ) ----------------
class Queue(models.Model):
    SECTOR_CHOICES = [
        ('Bank', 'Bank'),
        ('Library', 'Library'),
        ('Office', 'UAP Office'),
        ('Canteen', 'Canteen'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)

    token = models.CharField(max_length=10)
    position = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token} - {self.sector}"