import logging
from datetime import datetime
from typing import Dict, Any, List
from .constants import LOG_FORMAT, LOG_LEVEL

def setup_logging(name: str) -> logging.Logger:
    """Set up logging configuration for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def format_price(price: float) -> str:
    """Format price with currency symbol and two decimal places."""
    return f"${price:.2f}"

def parse_datetime(datetime_str: str) -> datetime:
    """Parse datetime string into datetime object."""
    try:
        return datetime.fromisoformat(datetime_str)
    except ValueError:
        return None

def clean_location(location: str) -> str:
    """Clean and standardize location string."""
    return location.strip().upper()

def validate_search_params(params: Dict[str, Any]) -> List[str]:
    """Validate search parameters and return list of errors."""
    errors = []
    
    # Check required fields
    required_fields = ['from_location', 'to_location']
    for field in required_fields:
        if not params.get(field):
            errors.append(f"{field} is required")
    
    # Validate location format
    if params.get('from_location'):
        if not clean_location(params['from_location']):
            errors.append("Invalid from_location format")
    
    if params.get('to_location'):
        if not clean_location(params['to_location']):
            errors.append("Invalid to_location format")
    
    # Validate date format if provided
    if params.get('date'):
        try:
            datetime.strptime(params['date'], '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date format. Use YYYY-MM-DD")
    
    return errors

def format_duration(duration: str) -> str:
    """Format flight duration string."""
    try:
        # Remove any extra spaces and standardize format
        return ' '.join(duration.split())
    except:
        return duration

def calculate_price_difference(price1: float, price2: float) -> Dict[str, Any]:
    """Calculate the difference between two prices."""
    difference = price2 - price1
    percentage = (difference / price1) * 100 if price1 > 0 else 0
    
    return {
        'absolute': round(difference, 2),
        'percentage': round(percentage, 2),
        'direction': 'increase' if difference > 0 else 'decrease'
    }

def format_flight_details(flight: Dict[str, Any]) -> Dict[str, Any]:
    """Format flight details for consistent output."""
    return {
        'airline': flight.get('airline', ''),
        'price': format_price(flight.get('price', 0)),
        'departure_time': flight.get('departure_time', ''),
        'arrival_time': flight.get('arrival_time', ''),
        'duration': format_duration(flight.get('duration', '')),
        'stops': flight.get('stops', ''),
        'source': flight.get('source', '')
    }

def group_flights_by_airline(flights: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group flights by airline."""
    grouped = {}
    for flight in flights:
        airline = flight.get('airline')
        if airline not in grouped:
            grouped[airline] = []
        grouped[airline].append(format_flight_details(flight))
    return grouped

def calculate_price_statistics(prices: List[float]) -> Dict[str, float]:
    """Calculate basic price statistics."""
    if not prices:
        return {
            'mean': 0,
            'median': 0,
            'min': 0,
            'max': 0
        }
    
    return {
        'mean': round(sum(prices) / len(prices), 2),
        'median': round(sorted(prices)[len(prices)//2], 2),
        'min': round(min(prices), 2),
        'max': round(max(prices), 2)
    } 