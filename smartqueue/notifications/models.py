from django.db import models

# Create your models here.
from django.db import models

class Notification(models.Model):
    student_id = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.student_id}: {self.message[:30]}"