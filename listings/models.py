from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
import pandas as pd

from listings.managers import ListingManager


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255, )
    country = models.CharField(max_length=255, )
    city = models.CharField(max_length=255, )

    objects = ListingManager()

    def __str__(self):
        return self.title

    def is_available_on_date(self, date):
        if self.listing_type == self.APARTMENT:
            if not ReservationInfo.objects.filter(listing=self, reserved_date=date).exists():
                try:
                    book_info_price = self.booking_info.price
                except:
                    book_info_price = 0
                return True, book_info_price
        else:
            hotel_rooms = HotelRoom.objects.filter(hotel_room_type__hotel=self)
            for room in hotel_rooms:
                if not ReservationInfo.objects.filter(hotel_room=room, reserved_date=date).exists():
                    try:
                        book_info_price = room.hotel_room_type.booking_info
                    except:
                        book_info_price = 0
                    return True, book_info_price

        return False, 0



class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255, )

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255, )

    def __str__(self):
        return self.room_number


class BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type

        return f'{obj} {self.price}'


class ReservationInfo(models.Model):
    reserved_date = models.DateField()
    listing = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='reservation_info'
    )
    hotel_room = models.ForeignKey(
        HotelRoom,
        on_delete=models.CASCADE,
        related_name='reservation_info',
        blank=True,
        null=True,
    )

    @classmethod
    def create_by_daterange(cls, from_date, to_date, **kwargs):
        daterange = pd.date_range(from_date, to_date)
        if from_date == to_date:
            return cls.objects.bulk_create([cls(reserved_date=from_date, **kwargs)])
        return cls.objects.bulk_create([cls(reserved_date=date, **kwargs) for date in daterange])
