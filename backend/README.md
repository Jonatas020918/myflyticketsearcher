# Flight Search Backend

A Django-based backend service for searching and analyzing flight prices from multiple sources.

## Features

- Flight search across multiple sources (Google Flights, Kayak)
- Price analysis and recommendations
- Price history tracking
- RESTful API endpoints
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- Chrome browser (for web scraping)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with the following variables:
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Flight Search
- `POST /api/flights/search/`
  - Request body:
    ```json
    {
      "from_location": "NYC",
      "to_location": "LAX"
    }
    ```
  - Returns flight results and price analysis

### Price History
- `GET /api/flights/{flight_id}/price_history/`
  - Returns price history for a specific flight

### Price Tips
- `GET /api/flights/price_tips/?from=NYC&to=LAX`
  - Returns price analysis and recommendations

## Project Structure

```
backend/
├── flight_search/          # Django project settings
├── flights/               # Main app
│   ├── services/         # Business logic
│   │   ├── scraper.py    # Web scraping service
│   │   └── price_analyzer.py  # Price analysis service
│   ├── utils/           # Utility functions
│   │   ├── constants.py # Constants and configurations
│   │   └── helpers.py   # Helper functions
│   ├── models.py        # Database models
│   ├── serializers.py   # API serializers
│   ├── views.py         # API views
│   └── urls.py          # URL routing
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use a code formatter like `black` to maintain consistent style:
```bash
pip install black
black .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 