# events/urls.py
from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView,
    EventUpdateView, EventDeleteView, RSVPView
)

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('create/', EventCreateView.as_view(), name='create'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/rsvp/', RSVPView.as_view(), name='rsvp'),
]
