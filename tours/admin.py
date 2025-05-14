from django.contrib import admin

from tours.models import Tour
from tours.models import Booking

admin.site.register(Tour)
admin.site.register(Booking)