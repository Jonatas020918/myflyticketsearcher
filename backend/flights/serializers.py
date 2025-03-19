from rest_framework import serializers
from .models import Flight, PriceHistory
from datetime import datetime, date

class PriceHistorySerializer(serializers.ModelSerializer):
    recorded_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    
    class Meta:
        model = PriceHistory
        fields = ['price', 'recorded_at']

class FlightSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)
    departure_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    arrival_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    
    class Meta:
        model = Flight
        fields = [
            'id', 'airline', 'price', 'departure_time', 'arrival_time',
            'duration', 'stops', 'source', 'created_at', 'updated_at',
            'price_history'
        ]
        read_only_fields = ['created_at', 'updated_at']

class FlightSearchSerializer(serializers.Serializer):
    from_location = serializers.CharField(max_length=3)
    to_location = serializers.CharField(max_length=3)
    initial_date = serializers.DateField(required=True)
    return_date = serializers.DateField(required=False, allow_null=True)

    def validate_initial_date(self, value):
        today = date.today()
        if value < today:
            raise serializers.ValidationError("Initial date cannot be in the past")
        return value

    def validate_return_date(self, value):
        initial_date = self.initial_data.get('initial_date')
        if initial_date:
            # Convert string to date if needed
            if isinstance(initial_date, str):
                initial_date = datetime.strptime(initial_date, '%Y-%m-%d').date()
            if value and value < initial_date:
                raise serializers.ValidationError("Return date must be after initial date")
        return value 