from django.db import models


class EmergencyRequest(models.Model):
    student_id = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency for {self.student_id}"


