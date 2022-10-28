from django.urls import path

from .views import EvenListAPIView, EventCreateAPIView, EventRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", EvenListAPIView.as_view(), name="event_list"),
    path("create/", EventCreateAPIView.as_view(), name="event_create"),
    path("event/<str:id>/", EventRetrieveUpdateDestroyAPIView.as_view(), name="event_update_delete_retrieve"),
]
