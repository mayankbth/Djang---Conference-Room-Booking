from django.urls import path
from .views import room, room_details, instructions


urlpatterns = [
    path('', room, name='room'),
    path('details/', room_details, name='room_details'),
    path('instructions/', instructions, name='instructions')
]