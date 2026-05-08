from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=20, default='customer')


class Service(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name


class Counter(models.Model):
    number = models.IntegerField(unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    def __str__(self): return f"Counter {self.number}"


class Queue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('serving', 'Serving'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    token_number = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Token {self.token_number}"