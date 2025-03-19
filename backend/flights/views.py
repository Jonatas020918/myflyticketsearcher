from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Min, Max
from datetime import datetime, timedelta
from .models import Flight, PriceHistory
from .serializers import FlightSerializer, PriceHistorySerializer, FlightSearchSerializer
from .services.scraper import FlightScraper
from .services.price_analyzer import PriceAnalyzer
import json

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        flight = self.get_object()
        history = PriceHistory.objects.filter(flight=flight).order_by('-recorded_at')
        return Response({
            'price_history': [
                {
                    'price': record.price,
                    'recorded_at': record.recorded_at.isoformat()
                }
                for record in history
            ]
        })

    @action(detail=False, methods=['post'])
    def search(self, request):
        try:
            # Parse JSON data
            data = request.data if isinstance(request.data, dict) else json.loads(request.body)
            
            serializer = FlightSearchSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'error': 'Invalid input data',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            from_location = serializer.validated_data['from_location']
            to_location = serializer.validated_data['to_location']
            initial_date = serializer.validated_data['initial_date']
            return_date = serializer.validated_data.get('return_date')

            # Format dates for the scraper
            initial_date_str = initial_date.strftime('%Y-%m-%d')
            return_date_str = return_date.strftime('%Y-%m-%d') if return_date else None

            # Scrape flights
            scraper = FlightScraper()
            scraped_flights = scraper.scrape_flights(
                from_location=from_location,
                to_location=to_location,
                initial_date=initial_date_str,
                return_date=return_date_str
            )

            # Save flights to database
            saved_flights = []
            for flight_data in scraped_flights:
                # Convert string times to datetime
                departure_time = datetime.strptime(
                    f"{initial_date_str} {flight_data['departure_time']}", 
                    '%Y-%m-%d %I:%M %p'
                )
                arrival_time = datetime.strptime(
                    f"{initial_date_str} {flight_data['arrival_time']}", 
                    '%Y-%m-%d %I:%M %p'
                )
                
                # Handle overnight flights
                if arrival_time < departure_time:
                    arrival_time = arrival_time + timedelta(days=1)

                # Create or update flight
                flight, created = Flight.objects.update_or_create(
                    airline=flight_data['airline'],
                    from_location=flight_data['from_location'],
                    to_location=flight_data['to_location'],
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    defaults={
                        'price': flight_data['price'],
                        'duration': flight_data['duration'],
                        'stops': flight_data['stops'],
                        'source': flight_data['source']
                    }
                )

                # Create price history record
                PriceHistory.objects.create(
                    flight=flight,
                    price=flight_data['price']
                )

                saved_flights.append(flight)

            # Get price tips
            price_analyzer = PriceAnalyzer()
            price_tips = price_analyzer.get_price_tips(from_location, to_location)

            # Serialize saved flights
            flight_serializer = FlightSerializer(saved_flights, many=True)

            return Response({
                'flights': flight_serializer.data,
                'price_tips': price_tips,
                'search_metadata': {
                    'from_location': from_location,
                    'to_location': to_location,
                    'initial_date': initial_date_str,
                    'return_date': return_date_str,
                    'total_results': len(saved_flights)
                }
            })

        except json.JSONDecodeError:
            return Response({
                'error': 'Invalid JSON data',
                'details': 'The request body must be valid JSON'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def price_tips(self, request):
        try:
            from_location = request.query_params.get('from')
            to_location = request.query_params.get('to')

            if not from_location or not to_location:
                return Response({
                    'error': 'Missing parameters',
                    'details': 'Both "from" and "to" parameters are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            price_analyzer = PriceAnalyzer()
            tips = price_analyzer.get_price_tips(from_location, to_location)

            return Response(tips)

        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
