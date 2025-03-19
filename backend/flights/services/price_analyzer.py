import statistics
from datetime import datetime, timedelta
from django.db.models import Avg, Min, Max
from ..models import Flight, PriceHistory
import logging

logger = logging.getLogger(__name__)

class PriceAnalyzer:
    def get_price_tips(self, from_location, to_location):
        """
        Get price tips and recommendations for a specific route
        """
        try:
            # Get historical price data for the route
            flights = Flight.objects.filter(
                from_location=from_location,
                to_location=to_location
            )
            
            if not flights.exists():
                return {
                    'average_price': None,
                    'recommendations': [
                        'No historical data available for this route',
                        'Consider checking multiple dates for better prices'
                    ]
                }
            
            # Calculate price statistics
            avg_price = flights.aggregate(Avg('price'))['price__avg']
            min_price = flights.aggregate(Min('price'))['price__min']
            max_price = flights.aggregate(Max('price'))['price__max']
            
            # Generate recommendations based on price analysis
            recommendations = []
            
            # Price range analysis
            price_range = max_price - min_price
            if price_range > 200:
                recommendations.append(f"Prices vary significantly (${min_price:.2f} - ${max_price:.2f}). Consider flexible dates.")
            
            # Booking time analysis
            for flight in flights:
                if flight.created_at:
                    days_before = (flight.departure_time.date() - flight.created_at.date()).days
                    if days_before >= 21:
                        recommendations.append("Booking 3 weeks in advance often yields better prices")
                    elif days_before <= 7:
                        recommendations.append("Last-minute bookings may be more expensive")
            
            # Day of week analysis
            weekday_prices = flights.filter(departure_time__weekday__lt=5).aggregate(Avg('price'))['price__avg']
            weekend_prices = flights.filter(departure_time__weekday__gte=5).aggregate(Avg('price'))['price__avg']
            
            if weekday_prices and weekend_prices:
                if weekday_prices < weekend_prices:
                    recommendations.append("Weekday flights are typically cheaper than weekend flights")
                else:
                    recommendations.append("Weekend flights might offer better value for this route")
            
            return {
                'average_price': round(avg_price, 2) if avg_price else None,
                'min_price': round(min_price, 2) if min_price else None,
                'max_price': round(max_price, 2) if max_price else None,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error getting price tips: {str(e)}")
            return {
                'average_price': None,
                'recommendations': [
                    'Unable to analyze prices at this time',
                    'Please try again later'
                ]
            }
            
    def analyze_prices(self, flights_data, from_location, to_location):
        """
        Analyze flight prices and generate insights
        """
        try:
            if not flights_data:
                return {
                    'average_price': None,
                    'recommendations': ['No flight data available for analysis']
                }
            
            # Calculate average price
            prices = [flight['price'] for flight in flights_data]
            avg_price = sum(prices) / len(prices)
            
            # Generate basic recommendations
            recommendations = []
            
            # Price range analysis
            min_price = min(prices)
            max_price = max(prices)
            if max_price - min_price > 200:
                recommendations.append(f"Prices vary significantly (${min_price:.2f} - ${max_price:.2f})")
            
            # Airline analysis
            airlines = {}
            for flight in flights_data:
                airline = flight['airline']
                if airline in airlines:
                    airlines[airline].append(flight['price'])
                else:
                    airlines[airline] = [flight['price']]
            
            # Find airline with best average price
            best_airline = min(airlines.items(), key=lambda x: sum(x[1])/len(x[1]))
            recommendations.append(f"{best_airline[0]} typically offers the best prices")
            
            return {
                'average_price': round(avg_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error analyzing prices: {str(e)}")
            return {
                'average_price': None,
                'recommendations': ['Unable to analyze prices at this time']
            }

    def _find_best_value_flights(self, flights_data):
        """Find flights that offer the best value (lowest price with reasonable duration)."""
        try:
            # Sort flights by price
            sorted_flights = sorted(flights_data, key=lambda x: x['price'])
            
            # Take top 3 flights
            best_value_flights = []
            for flight in sorted_flights[:3]:
                best_value_flights.append({
                    'airline': flight['airline'],
                    'price': round(flight['price'], 2),
                    'duration': flight['duration'],
                    'stops': flight['stops'],
                    'source': flight['source']
                })
            
            return best_value_flights
            
        except Exception as e:
            logger.error(f"Error finding best value flights: {str(e)}")
            return []

    def _analyze_price_trend(self, flights_data):
        """Analyze the price trend across different sources."""
        try:
            # Group flights by source
            source_prices = {}
            for flight in flights_data:
                source = flight['source']
                if source not in source_prices:
                    source_prices[source] = []
                source_prices[source].append(flight['price'])
            
            # Calculate average price for each source
            source_analysis = {}
            for source, prices in source_prices.items():
                source_analysis[source] = {
                    'average_price': round(statistics.mean(prices), 2),
                    'minimum_price': round(min(prices), 2),
                    'maximum_price': round(max(prices), 2),
                    'flight_count': len(prices)
                }
            
            return source_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing price trend: {str(e)}")
            return {}

    def _generate_recommendations(self, avg_price, min_price, max_price, price_range,
                                q1, q3, iqr, outliers, best_value_flights):
        """Generate price-related recommendations."""
        recommendations = []
        
        # Price range analysis
        if price_range > avg_price * 0.5:
            recommendations.append({
                'type': 'price_range',
                'message': 'There is significant price variation. Consider booking during off-peak times.',
                'severity': 'high'
            })
        
        # Outlier analysis
        if outliers:
            recommendations.append({
                'type': 'outliers',
                'message': f'Found {len(outliers)} unusually priced flights. These might be special deals or pricing errors.',
                'severity': 'medium'
            })
        
        # Best value analysis
        if best_value_flights:
            best_value = best_value_flights[0]
            if best_value['price'] < q1:
                recommendations.append({
                    'type': 'best_value',
                    'message': f'Found a great deal with {best_value["airline"]} at ${best_value["price"]}.',
                    'severity': 'low'
                })
        
        # Price trend analysis
        if q3 - q1 > avg_price * 0.3:
            recommendations.append({
                'type': 'price_trend',
                'message': 'Prices show significant variation. Consider monitoring prices for a few days.',
                'severity': 'medium'
            })
        
        return recommendations 