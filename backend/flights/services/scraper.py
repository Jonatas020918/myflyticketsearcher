from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup
import logging
import re
import random

logger = logging.getLogger(__name__)

class FlightScraper:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        chrome_options.add_argument('--disable-site-isolation-trials')
        chrome_options.add_argument('--disable-webgl')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--enable-unsafe-swiftshader')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set page load timeout
        self.driver.set_page_load_timeout(60)
        
        # Execute CDP commands to prevent detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": random.choice(user_agents)
        })
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
    def wait_for_page_load(self, timeout=60):
        """Wait for page to be fully loaded"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            return True
        except TimeoutException:
            logger.error("Timeout waiting for page to load")
            return False
            
    def wait_for_element(self, by, value, timeout=30, condition=EC.presence_of_element_located):
        """Wait for element to be present and visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                condition((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value}")
            return None
            
    def scrape_flights(self, from_location, to_location, initial_date, return_date=None):
        """
        Scrape flights from multiple sources for the specified date
        """
        flights_data = []
        search_date = datetime.strptime(initial_date, '%Y-%m-%d').date()
        logger.info(f"Scraping flights for date: {initial_date}")
        
        try:
            # Scrape from Google Flights
            logger.info(f"Scraping Google Flights for {from_location} to {to_location}")
            google_flights = self.scrape_google_flights(from_location, to_location, initial_date)
            if google_flights:
                for flight in google_flights:
                    flight['search_date'] = search_date
                flights_data.extend(google_flights)
            
            # Add delay between scraping different sources
            time.sleep(random.uniform(2, 5))
            
            # Scrape from Kayak
            logger.info(f"Scraping Kayak for {from_location} to {to_location}")
            kayak_flights = self.scrape_kayak(from_location, to_location, initial_date)
            if kayak_flights:
                for flight in kayak_flights:
                    flight['search_date'] = search_date
                flights_data.extend(kayak_flights)
            
            # Add delay between scraping different sources
            time.sleep(random.uniform(2, 5))
            
            # Scrape from Expedia
            logger.info(f"Scraping Expedia for {from_location} to {to_location}")
            expedia_flights = self.scrape_expedia(from_location, to_location, initial_date)
            if expedia_flights:
                for flight in expedia_flights:
                    flight['search_date'] = search_date
                flights_data.extend(expedia_flights)
            
            # Add delay between scraping different sources
            time.sleep(random.uniform(2, 5))
            
            # Scrape from Skyscanner
            logger.info(f"Scraping Skyscanner for {from_location} to {to_location}")
            skyscanner_flights = self.scrape_skyscanner(from_location, to_location, initial_date)
            if skyscanner_flights:
                for flight in skyscanner_flights:
                    flight['search_date'] = search_date
                flights_data.extend(skyscanner_flights)
            
            # Add delay between scraping different sources
            time.sleep(random.uniform(2, 5))
            
            # Scrape from major airlines
            airlines = [
                ('American Airlines', 'aa.com'),
                ('United Airlines', 'united.com'),
                ('Delta Air Lines', 'delta.com'),
                ('Southwest Airlines', 'southwest.com'),
                ('JetBlue', 'jetblue.com')
            ]
            
            for airline_name, airline_domain in airlines:
                logger.info(f"Scraping {airline_name} for {from_location} to {to_location}")
                airline_flights = self.scrape_airline(airline_name, airline_domain, from_location, to_location, initial_date)
                if airline_flights:
                    for flight in airline_flights:
                        flight['search_date'] = search_date
                    flights_data.extend(airline_flights)
                
                # Add delay between scraping different airlines
                time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            logger.error(f"Error scraping flights for date {initial_date}: {str(e)}")
        
        return flights_data
            
    def scrape_google_flights(self, from_location, to_location, initial_date):
        """Scrape flight data from Google Flights"""
        try:
            url = self._build_google_flights_url(from_location, to_location, initial_date)
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                return []
                
            # Wait for results container
            results_container = self.wait_for_element(
                By.CSS_SELECTOR, 
                "div[role='list']",
                timeout=60,
                condition=EC.presence_of_element_located
            )
            if not results_container:
                return []
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(3, 7))
            
            # Scroll to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            flights = []
            flight_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
            
            for element in flight_elements:
                try:
                    flight_data = self._parse_google_flight_element(element, from_location, to_location, initial_date)
                    if flight_data:
                        flights.append(flight_data)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing Google flight element: {str(e)}")
                    continue
            
            return flights
            
        except TimeoutException:
            logger.error("Timeout waiting for Google Flights results to load")
            return []
        except WebDriverException as e:
            logger.error(f"WebDriver error while scraping Google Flights: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping Google Flights: {str(e)}")
            return []
            
    def scrape_kayak(self, from_location, to_location, initial_date):
        """Scrape flight data from Kayak"""
        try:
            url = self._build_kayak_url(from_location, to_location, initial_date)
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                return []
                
            # Wait for results container
            results_container = self.wait_for_element(
                By.CLASS_NAME,
                "flight-result",
                timeout=60,
                condition=EC.presence_of_element_located
            )
            if not results_container:
                return []
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(3, 7))
            
            # Scroll to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            flights = []
            flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-result")
            
            for element in flight_elements:
                try:
                    flight_data = self._parse_kayak_flight_element(element, from_location, to_location, initial_date)
                    if flight_data:
                        flights.append(flight_data)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing Kayak flight element: {str(e)}")
                    continue
            
            return flights
            
        except TimeoutException:
            logger.error("Timeout waiting for Kayak results to load")
            return []
        except WebDriverException as e:
            logger.error(f"WebDriver error while scraping Kayak: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping Kayak: {str(e)}")
            return []
            
    def scrape_expedia(self, from_location, to_location, initial_date):
        """Scrape flight data from Expedia"""
        try:
            url = self._build_expedia_url(from_location, to_location, initial_date)
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                return []
                
            # Wait for results container
            results_container = self.wait_for_element(
                By.CLASS_NAME,
                "uitk-card",
                timeout=60,
                condition=EC.presence_of_element_located
            )
            if not results_container:
                return []
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(3, 7))
            
            # Scroll to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            flights = []
            flight_elements = self.driver.find_elements(By.CLASS_NAME, "uitk-card")
            
            for element in flight_elements:
                try:
                    flight_data = self._parse_expedia_flight_element(element, from_location, to_location, initial_date)
                    if flight_data:
                        flights.append(flight_data)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing Expedia flight element: {str(e)}")
                    continue
            
            return flights
            
        except TimeoutException:
            logger.error("Timeout waiting for Expedia results to load")
            return []
        except WebDriverException as e:
            logger.error(f"WebDriver error while scraping Expedia: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping Expedia: {str(e)}")
            return []
            
    def scrape_skyscanner(self, from_location, to_location, initial_date):
        """Scrape flight data from Skyscanner"""
        try:
            url = self._build_skyscanner_url(from_location, to_location, initial_date)
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                return []
                
            # Wait for results container
            results_container = self.wait_for_element(
                By.CLASS_NAME,
                "flight-card",
                timeout=60,
                condition=EC.presence_of_element_located
            )
            if not results_container:
                return []
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(3, 7))
            
            # Scroll to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            flights = []
            flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-card")
            
            for element in flight_elements:
                try:
                    flight_data = self._parse_skyscanner_flight_element(element, from_location, to_location, initial_date)
                    if flight_data:
                        flights.append(flight_data)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing Skyscanner flight element: {str(e)}")
                    continue
            
            return flights
            
        except TimeoutException:
            logger.error("Timeout waiting for Skyscanner results to load")
            return []
        except WebDriverException as e:
            logger.error(f"WebDriver error while scraping Skyscanner: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping Skyscanner: {str(e)}")
            return []
            
    def scrape_airline(self, airline_name, airline_domain, from_location, to_location, initial_date):
        """Scrape flight data from airline website"""
        try:
            url = self._build_airline_url(airline_domain, from_location, to_location, initial_date)
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                return []
                
            # Wait for results container (airline-specific selectors)
            results_container = self.wait_for_element(
                By.CLASS_NAME,
                "flight-results",  # This will need to be customized per airline
                timeout=60,
                condition=EC.presence_of_element_located
            )
            if not results_container:
                return []
            
            # Add random delay to simulate human behavior
            time.sleep(random.uniform(3, 7))
            
            # Scroll to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            flights = []
            flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-result")  # This will need to be customized per airline
            
            for element in flight_elements:
                try:
                    flight_data = self._parse_airline_flight_element(element, airline_name, from_location, to_location, initial_date)
                    if flight_data:
                        flights.append(flight_data)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing {airline_name} flight element: {str(e)}")
                    continue
            
            return flights
            
        except TimeoutException:
            logger.error(f"Timeout waiting for {airline_name} results to load")
            return []
        except WebDriverException as e:
            logger.error(f"WebDriver error while scraping {airline_name}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping {airline_name}: {str(e)}")
            return []
            
    def _build_google_flights_url(self, from_location, to_location, initial_date):
        """Build Google Flights URL"""
        base_url = "https://www.google.com/travel/flights"
        return f"{base_url}?q=Flights%20to%20{to_location}%20from%20{from_location}%20on%20{initial_date}"
            
    def _build_kayak_url(self, from_location, to_location, initial_date):
        """Build Kayak URL"""
        base_url = "https://www.kayak.com/flights"
        return f"{base_url}/{from_location}-{to_location}/{initial_date}"
            
    def _build_expedia_url(self, from_location, to_location, initial_date):
        """Build Expedia URL"""
        base_url = "https://www.expedia.com/search/flights"
        return f"{base_url}?from={from_location}&to={to_location}&date={initial_date}"
            
    def _build_skyscanner_url(self, from_location, to_location, initial_date):
        """Build Skyscanner URL"""
        base_url = "https://www.skyscanner.com/transport/flights"
        return f"{base_url}/{from_location}/{to_location}/{initial_date}"
            
    def _build_airline_url(self, airline_domain, from_location, to_location, initial_date):
        """Build airline website URL"""
        base_url = f"https://www.{airline_domain}"
        return f"{base_url}/flights/search?from={from_location}&to={to_location}&date={initial_date}"
            
    def _parse_google_flight_element(self, element, from_location, to_location, search_date):
        """Parse a Google Flights result element"""
        try:
            # Basic flight info with increased wait time
            wait = WebDriverWait(self.driver, 10)
            airline = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='link']"))
            ).text
            
            price_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[aria-label*='$']"))
            )
            price = float(re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_elem.text).group(1).replace(',', ''))
            
            # Time information
            time_elements = element.find_elements(By.CSS_SELECTOR, "div[role='text']")
            departure_time_str = time_elements[0].text
            arrival_time_str = time_elements[1].text
            
            # Parse times and create datetime objects
            departure_time = self._parse_time_string(departure_time_str, search_date)
            arrival_time = self._parse_time_string(arrival_time_str, search_date)
            
            # Handle overnight flights
            if arrival_time < departure_time:
                arrival_time += timedelta(days=1)
            
            # Flight details
            details_elem = element.find_element(By.CSS_SELECTOR, "div[class*='duration']")
            duration_match = re.search(r'(\d+h(?:\s*\d+m)?)', details_elem.text)
            duration = duration_match.group(1) if duration_match else "N/A"
            
            # Stops information
            stops_elem = element.find_element(By.CSS_SELECTOR, "div[class*='stops']")
            stops_text = stops_elem.text.lower()
            stops = 0 if 'nonstop' in stops_text else int(re.search(r'(\d+)', stops_text).group(1))
            
            # Additional information with error handling
            try:
                flight_number = element.find_element(By.CSS_SELECTOR, "div[class*='flight-number']").text
            except NoSuchElementException:
                flight_number = None
                
            try:
                aircraft_type = element.find_element(By.CSS_SELECTOR, "div[class*='aircraft']").text
            except NoSuchElementException:
                aircraft_type = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'from_location': from_location,
                'to_location': to_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price': price,
                'currency': 'USD',
                'stops': stops,
                'stop_locations': [],
                'cabin_class': 'Economy',
                'aircraft_type': aircraft_type,
                'carry_on_included': True,
                'checked_bags_included': 0,
                'source': 'Google Flights',
                'refundable': False
            }
            
        except Exception as e:
            logger.error(f"Error parsing Google flight element: {str(e)}")
            return None
            
    def _parse_kayak_flight_element(self, element, from_location, to_location, search_date):
        """Parse a Kayak flight result element"""
        try:
            # Basic flight info with increased wait time
            wait = WebDriverWait(self.driver, 10)
            airline = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "airline-name"))
            ).text
            
            price_elem = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "price-text"))
            )
            price = float(re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_elem.text).group(1).replace(',', ''))
            
            # Time information
            time_elements = element.find_elements(By.CLASS_NAME, "time")
            departure_time_str = time_elements[0].text
            arrival_time_str = time_elements[1].text
            
            # Parse times and create datetime objects
            departure_time = self._parse_time_string(departure_time_str, search_date)
            arrival_time = self._parse_time_string(arrival_time_str, search_date)
            
            # Handle overnight flights
            if arrival_time < departure_time:
                arrival_time += timedelta(days=1)
            
            # Duration and stops
            duration_elem = element.find_element(By.CLASS_NAME, "duration")
            duration = duration_elem.text.strip()
            
            stops_elem = element.find_element(By.CLASS_NAME, "stops-text")
            stops_text = stops_elem.text.lower()
            stops = 0 if 'nonstop' in stops_text else int(re.search(r'(\d+)', stops_text).group(1))
            
            # Additional information with error handling
            try:
                flight_number = element.find_element(By.CLASS_NAME, "flight-number").text
            except NoSuchElementException:
                flight_number = None
                
            try:
                aircraft_type = element.find_element(By.CLASS_NAME, "aircraft-type").text
            except NoSuchElementException:
                aircraft_type = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'from_location': from_location,
                'to_location': to_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price': price,
                'currency': 'USD',
                'stops': stops,
                'stop_locations': [],
                'cabin_class': 'Economy',
                'aircraft_type': aircraft_type,
                'carry_on_included': True,
                'checked_bags_included': 0,
                'source': 'Kayak',
                'refundable': False
            }
            
        except Exception as e:
            logger.error(f"Error parsing Kayak flight element: {str(e)}")
            return None
            
    def _parse_expedia_flight_element(self, element, from_location, to_location, search_date):
        """Parse an Expedia flight result element"""
        try:
            # Basic flight info with increased wait time
            wait = WebDriverWait(self.driver, 10)
            airline = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "uitk-text"))
            ).text
            
            price_elem = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "uitk-price"))
            )
            price = float(re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_elem.text).group(1).replace(',', ''))
            
            # Time information
            time_elements = element.find_elements(By.CLASS_NAME, "uitk-time")
            departure_time_str = time_elements[0].text
            arrival_time_str = time_elements[1].text
            
            # Parse times and create datetime objects
            departure_time = self._parse_time_string(departure_time_str, search_date)
            arrival_time = self._parse_time_string(arrival_time_str, search_date)
            
            # Handle overnight flights
            if arrival_time < departure_time:
                arrival_time += timedelta(days=1)
            
            # Duration and stops
            duration_elem = element.find_element(By.CLASS_NAME, "uitk-duration")
            duration = duration_elem.text.strip()
            
            stops_elem = element.find_element(By.CLASS_NAME, "uitk-stops")
            stops_text = stops_elem.text.lower()
            stops = 0 if 'nonstop' in stops_text else int(re.search(r'(\d+)', stops_text).group(1))
            
            # Additional information with error handling
            try:
                flight_number = element.find_element(By.CLASS_NAME, "uitk-flight-number").text
            except NoSuchElementException:
                flight_number = None
                
            try:
                aircraft_type = element.find_element(By.CLASS_NAME, "uitk-aircraft").text
            except NoSuchElementException:
                aircraft_type = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'from_location': from_location,
                'to_location': to_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price': price,
                'currency': 'USD',
                'stops': stops,
                'stop_locations': [],
                'cabin_class': 'Economy',
                'aircraft_type': aircraft_type,
                'carry_on_included': True,
                'checked_bags_included': 0,
                'source': 'Expedia',
                'refundable': False
            }
            
        except Exception as e:
            logger.error(f"Error parsing Expedia flight element: {str(e)}")
            return None
            
    def _parse_skyscanner_flight_element(self, element, from_location, to_location, search_date):
        """Parse a Skyscanner flight result element"""
        try:
            # Basic flight info with increased wait time
            wait = WebDriverWait(self.driver, 10)
            airline = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "airline-name"))
            ).text
            
            price_elem = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            price = float(re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_elem.text).group(1).replace(',', ''))
            
            # Time information
            time_elements = element.find_elements(By.CLASS_NAME, "time")
            departure_time_str = time_elements[0].text
            arrival_time_str = time_elements[1].text
            
            # Parse times and create datetime objects
            departure_time = self._parse_time_string(departure_time_str, search_date)
            arrival_time = self._parse_time_string(arrival_time_str, search_date)
            
            # Handle overnight flights
            if arrival_time < departure_time:
                arrival_time += timedelta(days=1)
            
            # Duration and stops
            duration_elem = element.find_element(By.CLASS_NAME, "duration")
            duration = duration_elem.text.strip()
            
            stops_elem = element.find_element(By.CLASS_NAME, "stops")
            stops_text = stops_elem.text.lower()
            stops = 0 if 'nonstop' in stops_text else int(re.search(r'(\d+)', stops_text).group(1))
            
            # Additional information with error handling
            try:
                flight_number = element.find_element(By.CLASS_NAME, "flight-number").text
            except NoSuchElementException:
                flight_number = None
                
            try:
                aircraft_type = element.find_element(By.CLASS_NAME, "aircraft-type").text
            except NoSuchElementException:
                aircraft_type = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'from_location': from_location,
                'to_location': to_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price': price,
                'currency': 'USD',
                'stops': stops,
                'stop_locations': [],
                'cabin_class': 'Economy',
                'aircraft_type': aircraft_type,
                'carry_on_included': True,
                'checked_bags_included': 0,
                'source': 'Skyscanner',
                'refundable': False
            }
            
        except Exception as e:
            logger.error(f"Error parsing Skyscanner flight element: {str(e)}")
            return None
            
    def _parse_airline_flight_element(self, element, airline_name, from_location, to_location, search_date):
        """Parse an airline website flight result element"""
        try:
            # Basic flight info with increased wait time
            wait = WebDriverWait(self.driver, 10)
            airline = airline_name
            
            price_elem = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            price = float(re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_elem.text).group(1).replace(',', ''))
            
            # Time information
            time_elements = element.find_elements(By.CLASS_NAME, "time")
            departure_time_str = time_elements[0].text
            arrival_time_str = time_elements[1].text
            
            # Parse times and create datetime objects
            departure_time = self._parse_time_string(departure_time_str, search_date)
            arrival_time = self._parse_time_string(arrival_time_str, search_date)
            
            # Handle overnight flights
            if arrival_time < departure_time:
                arrival_time += timedelta(days=1)
            
            # Duration and stops
            duration_elem = element.find_element(By.CLASS_NAME, "duration")
            duration = duration_elem.text.strip()
            
            stops_elem = element.find_element(By.CLASS_NAME, "stops")
            stops_text = stops_elem.text.lower()
            stops = 0 if 'nonstop' in stops_text else int(re.search(r'(\d+)', stops_text).group(1))
            
            # Additional information with error handling
            try:
                flight_number = element.find_element(By.CLASS_NAME, "flight-number").text
            except NoSuchElementException:
                flight_number = None
                
            try:
                aircraft_type = element.find_element(By.CLASS_NAME, "aircraft-type").text
            except NoSuchElementException:
                aircraft_type = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'from_location': from_location,
                'to_location': to_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price': price,
                'currency': 'USD',
                'stops': stops,
                'stop_locations': [],
                'cabin_class': 'Economy',
                'aircraft_type': aircraft_type,
                'carry_on_included': True,
                'checked_bags_included': 0,
                'source': airline_name,
                'refundable': False
            }
            
        except Exception as e:
            logger.error(f"Error parsing {airline_name} flight element: {str(e)}")
            return None
            
    def _parse_time_string(self, time_str, search_date):
        """Parse time string into datetime object"""
        try:
            # Handle different time formats
            time_patterns = [
                r'(\d{1,2}):(\d{2})\s*(AM|PM)',  # 12-hour format
                r'(\d{1,2}):(\d{2})',  # 24-hour format
            ]
            
            for pattern in time_patterns:
                match = re.search(pattern, time_str)
                if match:
                    if len(match.groups()) == 3:  # 12-hour format
                        hour, minute, period = match.groups()
                        hour = int(hour)
                        if period == 'PM' and hour != 12:
                            hour += 12
                        elif period == 'AM' and hour == 12:
                            hour = 0
                    else:  # 24-hour format
                        hour, minute = map(int, match.groups())
                    
                    return datetime.combine(search_date, datetime.min.time().replace(hour=hour, minute=minute))
            
            raise ValueError(f"Could not parse time string: {time_str}")
            
        except Exception as e:
            logger.error(f"Error parsing time string: {str(e)}")
            return None
            
    def __del__(self):
        """Clean up WebDriver when the object is destroyed"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing WebDriver: {str(e)}") 