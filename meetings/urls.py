from django.urls import path

from meetings import views

urlpatterns = [
    path('', views.home, name='home'),
    path('staff', views.staff, name='staff'),
    path('meetings', views.meetings, name='meetings'),
    path('meetings/<slug:meeting_number>', views.meeting, name='meeting'),
    path('meetings/<slug:meeting_number>/new', views.create_meeting, name='create_meeting'),
    path('meetings/<slug:meeting_number>/items/<int:id>/status', views.items, name='items'),
    path('meetings/<slug:meeting_number>/items/<int:id>/history', views.history, name='history'),
    path('ajax/get_item_details', views.get_item_details, name='get_item_details')
]
