from django.db import models


class ListingManager(models.Manager):
    def availables(self, date):
        # available_ids = [listing.id for listing in self.all() if listing.is_available_on_date(date=date)[0]]
        # availables = self.filter(id__in=available_ids)
        availables = []
        for listing in self.all():
            is_available_on_date = listing.is_available_on_date(date)
            is_available = is_available_on_date[0]
            booking_price = is_available_on_date[1]
            if is_available:
                listing.booking_info_price = booking_price
                availables.append(listing)
        return availables

