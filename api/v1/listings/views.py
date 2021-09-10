import datetime

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.listings.serializers import ReservationInfoListSerializer, ReservationInfoCreateSerializer, AvailableListingSerializer
from api.v1.listings.validators import HotelRoomValidators
from listings.models import ReservationInfo, Listing


class ReservationInfoListAPIView(generics.ListAPIView):
    queryset = ReservationInfo.objects.all()
    serializer_class = ReservationInfoListSerializer


class ReservationInfoCreateView(APIView):
    serializer_class = ReservationInfoCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservations = serializer.save()
        result = self.serializer_class(reservations, many=True).data
        return Response({'result': result})


class AvailableListingsListView(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = AvailableListingSerializer

