from django.urls import path

from api.v1.listings.views import ReservationInfoListAPIView, ReservationInfoCreateView

urlpatterns = [
    path('reservations/list/', ReservationInfoListAPIView.as_view()),
    path('reservations/create/', ReservationInfoCreateView.as_view())
]
