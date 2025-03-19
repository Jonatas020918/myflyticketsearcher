# MyFlyTicketSearcher (v1.0-beta)

A comprehensive flight ticket search application that aggregates flight information from multiple sources including major airlines and travel agencies. This is currently in beta stage (v1.0) and requires several enhancements for production use.

## Current Status

This project is in active development. While the core functionality is implemented, there are known limitations and areas that need improvement:

### Known Limitations
- Selenium WebDriver stability issues with some flight search websites
- Timeout errors when scraping certain airlines
- Limited error handling for website changes
- Performance optimizations needed for concurrent scraping
- Browser compatibility issues need to be addressed

### Planned Enhancements
- Implement robust error handling and retry mechanisms
- Add support for proxy rotation to avoid rate limiting
- Improve scraping reliability with better selectors and wait conditions
- Add support for multiple browsers besides Chrome
- Implement caching to improve response times
- Add more comprehensive logging and monitoring
- Enhance the anti-detection mechanisms
- Add support for more airlines and travel websites

## Features

Current implementation includes:
- Search flights from multiple sources:
  - Google Flights
  - Kayak
  - Expedia
  - Skyscanner
  - Major Airlines (American Airlines, United Airlines, Delta Air Lines, Southwest Airlines, JetBlue)
- Real-time price comparison
- Detailed flight information including:
  - Flight numbers
  - Departure and arrival times
  - Duration
  - Number of stops
  - Aircraft type
  - Baggage information
  - Cabin class
  - Price history tracking

## Tech Stack

- Backend:
  - Python 3.x
  - Django
  - Selenium WebDriver
  - BeautifulSoup4
  - PostgreSQL

- Frontend:
  - React
  - Material-UI
  - Axios

## Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL
- Chrome browser (for Selenium WebDriver)
- Stable internet connection with good bandwidth (for reliable scraping)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jonatas020918/myflyticketsearcher.git
cd myflyticketsearcher
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm start
```

## Configuration

1. Create a `.env` file in the backend directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

2. Update the frontend configuration in `frontend/src/config.js` with your backend API URL.

## Usage

Note: Due to the current limitations, please be aware that some searches might timeout or return incomplete results.

1. Start the backend server:
```bash
cd backend
python manage.py runserver
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

4. Enter your search criteria:
   - From location
   - To location
   - Departure date
   - Return date (optional)

5. Click "Search" to find available flights

## Troubleshooting

Common issues and solutions:
1. Timeout errors:
   - Ensure stable internet connection
   - Try reducing the number of sources being searched
   - Increase timeout values in the configuration

2. Scraping failures:
   - Check if the target website is accessible
   - Verify Chrome WebDriver is up to date
   - Clear browser cache and cookies

3. Performance issues:
   - Ensure adequate system resources
   - Consider running fewer concurrent searches
   - Check database connection and performance

## API Endpoints

- `POST /api/flights/search/`: Search for flights
- `GET /api/flights/price-history/`: Get price history for a specific flight
- `GET /api/flights/airlines/`: Get list of supported airlines

## Contributing

This project needs community support to reach production quality. Areas where you can contribute:
1. Improving scraping reliability
2. Adding support for more flight sources
3. Enhancing error handling
4. Implementing caching mechanisms
5. Adding tests and documentation

To contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all the flight search websites and airlines for providing their data
- The open-source community for the tools and libraries used in this project

## Disclaimer

This is a beta version (v1.0) and should not be used in production without proper testing and enhancement. The application may have stability issues and incomplete features. Use at your own risk. 