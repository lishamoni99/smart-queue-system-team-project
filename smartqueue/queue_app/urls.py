from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student-login/', views.student_login, name='student_login'),
    path('sector-select/', views.sector_select, name='sector_select'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    path('guardian-login/', views.guardian_login, name='guardian_login'),
    path('guardian-dashboard/', views.guardian_dashboard, name='guardian_dashboard'),
    path('cancel-token/', views.cancel_token, name='cancel_token'),
    path('logout/', views.logout_view, name='logout'),
]