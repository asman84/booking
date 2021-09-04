from rest_framework import serializers
from rest_framework.exceptions import NotFound, NotAcceptable

from listings.models import HotelRoom, ReservationInfo


class HotelRoomValidators:

    @classmethod
    def is_valid_hotel_room(cls, hotel_room_id):
        try:
            hotel_room = HotelRoom.objects.get(id=hotel_room_id)
            return hotel_room
        except:
            raise NotFound('hotel room is not found')


class CheckDateRangeReservationValidator:
    def check_start_end_date(self, attr):
        reservation_start_date = attr.get('reservation_start_date')
        reservation_end_date = attr.get('reservation_end_date')
        if reservation_start_date > reservation_end_date:
            raise NotAcceptable("reservation start date is greater than reservation end date")

    def check_range_reservation(self, attr):
        reservation_start_date = attr.get('reservation_start_date')
        reservation_end_date = attr.get('reservation_end_date')
        if ReservationInfo.objects.filter(reserved_date__range=[reservation_start_date, reservation_end_date]).exists():
            raise NotAcceptable("room is reserved between this range")

    def __call__(self, attr):
        self.check_start_end_date(attr)
        self.check_range_reservation(attr)
