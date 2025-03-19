# API Response Status Codes
STATUS_SUCCESS = 200
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500

# Flight Search Parameters
MAX_RESULTS = 50
DEFAULT_PAGE_SIZE = 10

# Price Analysis Constants
PRICE_OUTLIER_THRESHOLD = 1.5  # IQR multiplier for outlier detection
SIGNIFICANT_PRICE_VARIATION = 0.5  # 50% of average price
PRICE_TREND_THRESHOLD = 0.3  # 30% of average price

# Time Constants
DEFAULT_TIMEOUT = 10  # seconds
PAGE_LOAD_DELAY = 3  # seconds

# Error Messages
ERROR_NO_FLIGHTS = "No flights found for the specified criteria"
ERROR_INVALID_PARAMETERS = "Invalid search parameters provided"
ERROR_SCRAPING_FAILED = "Failed to fetch flight data from one or more sources"
ERROR_ANALYSIS_FAILED = "Failed to analyze flight prices"

# Success Messages
SUCCESS_SEARCH_COMPLETE = "Flight search completed successfully"
SUCCESS_ANALYSIS_COMPLETE = "Price analysis completed successfully"

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO' 