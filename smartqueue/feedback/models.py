from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)

    comment = models.TextField()

    image = models.ImageField(upload_to='feedback_images/')

    def __str__(self):
        return self.name