import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.v1.listings.validators import CheckDateRangeReservationValidator
from listings.models import ReservationInfo, Listing


class ReservationInfoListSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='hotel_room.room_number')
    hotel_title = serializers.SerializerMethodField()
    room_price = serializers.SerializerMethodField()

    class Meta:
        model = ReservationInfo
        fields = [
            'id',
            'listing',
            'hotel_title',
            'room_number',
            'room_price',
            'reserved_date'
        ]

    def get_hotel_title(self, value):
        try:
            return value.hotel_room.hotel_room_type.hotel.title
        except:
            return ""

    def get_room_price(self, value):
        try:
            return value.hotel_room.hotel_room_type.booking_info.price
        except:
            return 0


class ReservationInfoCreateSerializer(serializers.ModelSerializer):
    listing_info = serializers.CharField(source='listing.title', read_only=True)
    reserved_date = serializers.DateTimeField(read_only=True)
    check_in_date = serializers.DateField(required=False)
    check_out_date = serializers.DateField(required=False)

    class Meta:
        model = ReservationInfo
        fields = [
            "listing",
            "listing_info",
            "hotel_room",
            "reserved_date",
            "check_in_date",
            "check_out_date",
        ]

        validators = [
            CheckDateRangeReservationValidator()
        ]

    def create(self, validated_data):
        check_in_date = validated_data.pop("check_in_date")
        check_out_date = validated_data.pop("check_out_date")
        check_out_date = check_out_date - datetime.timedelta(days=1)
        t = datetime.time(0, 0)
        check_out_date = datetime.datetime.combine(check_out_date, t)
        reservations = ReservationInfo.create_by_daterange(check_in_date, check_out_date, **validated_data)
        return reservations


class AvailableListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields =[
            'id',
            'listing_type',
            'title',
            'country',
            'city',

        ]



