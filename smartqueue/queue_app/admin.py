from django.contrib import admin
from .models import Student, Guardian

admin.site.register(Student)
admin.site.register(Guardian)