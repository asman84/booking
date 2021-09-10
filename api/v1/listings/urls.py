from django.urls import path

from api.v1.listings.views import ReservationInfoListAPIView, ReservationInfoCreateView, AvailableListingsListView

urlpatterns = [
    path('reservations/list/', ReservationInfoListAPIView.as_view()),
    path('reservations/create/', ReservationInfoCreateView.as_view()),
    path('available-rooms/list/', AvailableListingsListView.as_view()),
]
