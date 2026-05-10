from django.contrib import admin
from queue_app.models import Queue


try:
    admin.site.unregister(Queue)
except admin.sites.NotRegistered:
    pass

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):

    list_display = ('token', 'sector', 'position')
    fields = ('student', 'sector', 'token', 'position')