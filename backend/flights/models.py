from django.db import models
from django.utils import timezone

# Create your models here.

class Flight(models.Model):
    # Basic flight information
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20, blank=True, null=True)
    from_location = models.CharField(max_length=3)
    to_location = models.CharField(max_length=3)
    
    # Time information
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.CharField(max_length=20)  # Format: "XhYm"
    
    # Price information
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Route information
    stops = models.IntegerField(default=0)
    stop_locations = models.JSONField(default=list, blank=True)  # List of airport codes
    
    # Additional information
    cabin_class = models.CharField(max_length=50, default='Economy')
    seats_available = models.IntegerField(null=True, blank=True)
    aircraft_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Baggage information
    carry_on_included = models.BooleanField(default=True)
    checked_bags_included = models.IntegerField(default=0)
    
    # Booking information
    booking_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=50)  # e.g., 'Google Flights', 'Kayak'
    refundable = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_date = models.DateField(default=timezone.now)  # The date for which this flight was searched

    def __str__(self):
        return f"{self.airline} {self.flight_number} - {self.from_location} to {self.to_location} on {self.departure_time.date()}"

    class Meta:
        ordering = ['price', 'departure_time']
        indexes = [
            models.Index(fields=['from_location', 'to_location', 'departure_time']),
            models.Index(fields=['price']),
            models.Index(fields=['airline']),
        ]

class PriceHistory(models.Model):
    flight = models.ForeignKey(Flight, related_name='price_history', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    recorded_at = models.DateTimeField(auto_now_add=True)
    search_date = models.DateField(default=timezone.now)  # The date for which the price was recorded

    def __str__(self):
        return f"{self.flight.airline} - ${self.price} for {self.search_date}"

    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['flight', 'recorded_at']),
            models.Index(fields=['search_date']),
        ]
