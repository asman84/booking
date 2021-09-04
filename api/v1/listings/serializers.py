from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.v1.listings.validators import CheckDateRangeReservationValidator
from listings.models import ReservationInfo


class ReservationInfoListSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='hotel_room.room_number')
    hotel_title = serializers.SerializerMethodField()
    room_price = serializers.SerializerMethodField()

    class Meta:
        model = ReservationInfo
        fields = [
            'id',
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


from django.utils.translation import ugettext_lazy as _




class ReservationInfoCreateSerializer(serializers.ModelSerializer):
    reservation_start_date = serializers.DateField(required=False)
    reservation_end_date = serializers.DateField(required=False)

    class Meta:
        model = ReservationInfo
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=ReservationInfo.objects.all(),
                fields=('reserved_date', 'hotel_room'),
                message=_("this hotel room/apartment is reserved for chosen date.")
            ),
            CheckDateRangeReservationValidator()
        ]

    def create(self, validated_data):
        validated_data.pop('reservation_start_date')
        validated_data.pop('reservation_end_date')

        return super().create(validated_data)
