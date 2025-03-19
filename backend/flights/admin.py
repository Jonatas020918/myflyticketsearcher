from django.contrib import admin
from .models import Flight, PriceHistory

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('airline', 'from_location', 'to_location', 'price', 'departure_time', 'arrival_time', 'duration', 'stops', 'source')
    list_filter = ('airline', 'source', 'stops')
    search_fields = ('airline', 'from_location', 'to_location')
    ordering = ('price', 'departure_time')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('flight', 'price', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('flight__airline',)
    ordering = ('-recorded_at',)
