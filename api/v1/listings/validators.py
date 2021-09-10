from rest_framework import serializers
from rest_framework.exceptions import NotFound, NotAcceptable

from listings.models import HotelRoom, ReservationInfo, Listing


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
        check_in_date = attr.get('check_in_date')
        check_out_date = attr.get('check_out_date')
        if check_in_date >= check_out_date:
            raise NotAcceptable("check_in_date is greater than check_out_date or both are equal")

    def check_hotel_room_apartment_existance(self, attr):
        """to check either hotel room id or listing id is in sent data"""
        hotel_room = attr.get('hotel_room')
        listing = attr.get('listing')
        if (hotel_room and listing) or (not hotel_room and not listing):
            raise NotAcceptable("either hotel room or listing should be given")

    def check_listing_is_apartment(self, attr):
        """to check if the listing type is apartment """
        listing = attr.get('listing')
        if listing and not listing.listing_type == Listing.APARTMENT:
            raise NotAcceptable("listing type is not apartment")

    def check_range_reservation(self, attr):
        check_in_date = attr.get('check_in_date')
        check_out_date = attr.get('check_out_date')
        hotel_room = attr.get('hotel_room')
        listing = attr.get('listing')
        filter_data = dict(
            listing=listing,
            hotel_room=hotel_room,
            reserved_date__range=[check_in_date, check_out_date]
        )
        if ReservationInfo.objects.filter(**filter_data).exists():
            raise NotAcceptable("room is reserved between this range")

    def __call__(self, attr):
        self.check_start_end_date(attr)
        self.check_hotel_room_apartment_existance(attr)
        self.check_listing_is_apartment(attr)
        self.check_range_reservation(attr)
