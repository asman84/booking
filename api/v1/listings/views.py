import datetime

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.v1.listings.serializers import ReservationInfoListSerializer,ReservationInfoCreateSerializer
from api.v1.listings.validators import HotelRoomValidators
from listings.models import ReservationInfo


class ReservationInfoListAPIView(generics.ListAPIView):
    queryset = ReservationInfo.objects.all()
    serializer_class = ReservationInfoListSerializer


class ReservationInfoCreateAPIView2(generics.CreateAPIView):
    serializer_class = ReservationInfoCreateSerializer


class ReservationInfoCreateView(generics.CreateAPIView):
    serializer_class = ReservationInfoCreateSerializer