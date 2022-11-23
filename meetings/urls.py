from django.urls import path

from meetings import views

urlpatterns = [
    path('',views.home, name='home'),
    path('meetings',views.meetings, name='meetings'),
    path('staff',views.staff, name='staff'),
    path('reports',views.reports, name='reports')
]