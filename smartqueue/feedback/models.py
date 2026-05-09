from django.db import models

class Feedback(models.Model):
    student_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='feedback_images/' , null=True, blank=True)

    def __str__(self):
        return self.student_name

# Create your models here.
