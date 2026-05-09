from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('call-next/', views.call_next, name='call_next'),
    path('cancel-tomorrow/', views.cancel_tomorrow, name='cancel_tomorrow'),
]