from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Flight, PriceHistory
from .utils.helpers import (
    format_price,
    clean_location,
    validate_search_params,
    format_duration,
    calculate_price_difference
)

class FlightTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.flight = Flight.objects.create(
            airline="Test Airlines",
            price=299.99,
            departure_time="10:00",
            arrival_time="12:00",
            duration="2h",
            stops="Direct"
        )

    def test_flight_creation(self):
        """Test flight creation."""
        self.assertEqual(self.flight.airline, "Test Airlines")
        self.assertEqual(self.flight.price, 299.99)
        self.assertEqual(self.flight.duration, "2h")

    def test_price_history(self):
        """Test price history creation."""
        PriceHistory.objects.create(
            flight=self.flight,
            price=299.99
        )
        self.assertEqual(self.flight.price_history.count(), 1)
        self.assertEqual(self.flight.price_history.first().price, 299.99)

class FlightAPITests(APITestCase):
    def setUp(self):
        """Set up test data."""
        self.flight = Flight.objects.create(
            airline="Test Airlines",
            price=299.99,
            departure_time="10:00",
            arrival_time="12:00",
            duration="2h",
            stops="Direct"
        )
        self.url = reverse('flight-list')

    def test_get_flights(self):
        """Test getting list of flights."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_flights(self):
        """Test flight search endpoint."""
        url = reverse('flight-search')
        data = {
            'from_location': 'NYC',
            'to_location': 'LAX'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class HelperFunctionTests(TestCase):
    def test_format_price(self):
        """Test price formatting."""
        self.assertEqual(format_price(299.99), "$299.99")
        self.assertEqual(format_price(1000), "$1000.00")

    def test_clean_location(self):
        """Test location cleaning."""
        self.assertEqual(clean_location("  nyc  "), "NYC")
        self.assertEqual(clean_location("lax"), "LAX")

    def test_validate_search_params(self):
        """Test search parameter validation."""
        # Test missing required fields
        params = {}
        errors = validate_search_params(params)
        self.assertEqual(len(errors), 2)
        self.assertIn("from_location is required", errors)
        self.assertIn("to_location is required", errors)

        # Test valid parameters
        params = {
            'from_location': 'NYC',
            'to_location': 'LAX'
        }
        errors = validate_search_params(params)
        self.assertEqual(len(errors), 0)

    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration("2h 30m"), "2h 30m")
        self.assertEqual(format_duration("  3h  "), "3h")

    def test_calculate_price_difference(self):
        """Test price difference calculation."""
        result = calculate_price_difference(100, 120)
        self.assertEqual(result['absolute'], 20)
        self.assertEqual(result['percentage'], 20)
        self.assertEqual(result['direction'], 'increase')

        result = calculate_price_difference(100, 80)
        self.assertEqual(result['absolute'], -20)
        self.assertEqual(result['percentage'], -20)
        self.assertEqual(result['direction'], 'decrease')
