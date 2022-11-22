from django.urls import path

from meetings import views

urlpatterns = [
    path('',views.home, name='home')
]