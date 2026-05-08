from django.contrib import admin
from .models import User, Service, Counter, Queue

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Counter)
admin.site.register(Queue)