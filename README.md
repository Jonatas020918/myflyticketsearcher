# MyFlyTicketSearcher

A comprehensive flight ticket search application that aggregates flight information from multiple sources including major airlines and travel agencies.

## Features

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

## API Endpoints

- `POST /api/flights/search/`: Search for flights
- `GET /api/flights/price-history/`: Get price history for a specific flight
- `GET /api/flights/airlines/`: Get list of supported airlines

## Contributing

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