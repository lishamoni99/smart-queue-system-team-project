from django.db import models


class QueueHistory(models.Model):

    user_type = models.CharField(max_length=20)
    # "student" or "guardian"

    student_id = models.CharField(max_length=100, null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    token_number = models.CharField(max_length=20)

    sector = models.CharField(max_length=100)

    waiting_time = models.IntegerField()

    service_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_type