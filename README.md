# Air Quality Checker

A minimal Django web app that allows users to enter a location (city, state/province/region, and country or just city and state for USA) and fetches the current Air Quality Index (AQI) and related air quality data using the Open-Meteo Air Quality API. Geocoding is performed using the Nominatim OpenStreetMap API. The app includes form validation, error handling, and a simple web interface.

## Features
- Enter a location and get real-time AQI and pollutant data
- Uses public APIs (no API keys required)
- Client-side and server-side validation
- Graceful error handling for API and input issues
- Unit and integration tests for core logic and views

## Requirements
- Python 3.8+
- Django 4.x or 5.x
- requests

## Setup
1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd AirQualityChecker-guided
   ```
2. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   # or, if requirements.txt is missing:
   pip install django requests
   ```
4. **Apply database migrations**
   ```sh
   python manage.py migrate
   ```

## Running the App
Start the Django development server:
```sh
source venv/bin/activate
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Testing
Run the test suite (unit and integration tests):
```sh
source venv/bin/activate
python manage.py test checker
```

## Project Structure
- `checker/forms.py` — Django form for location input
- `checker/views.py` — Main view logic for form and results
- `checker/utils.py` — Utility functions for geocoding and AQI API
- `checker/templates/checker/location_form.html` — Main template
- `checker/tests.py` — Unit and integration tests
- `.github/instructions/` — Project and engineering guidance for Copilot/agents

## Notes
- The app uses only public APIs and does not require authentication.
- For best results, enter a valid city and state (and country if outside the USA).
- See `.github/instructions/` for project coding standards and best practices.

---

© 2025 Air Quality Checker Project
