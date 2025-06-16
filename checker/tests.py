from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .forms import LocationForm
from .utils import geocode_location, fetch_air_quality

class LocationFormTests(TestCase):
    def test_valid_form(self):
        form = LocationForm({"city": "San Francisco", "state": "CA", "country": "USA"})
        self.assertTrue(form.is_valid())

    def test_missing_city(self):
        form = LocationForm({"city": "", "state": "CA", "country": "USA"})
        self.assertFalse(form.is_valid())

    def test_missing_state(self):
        form = LocationForm({"city": "San Francisco", "state": "", "country": "USA"})
        self.assertFalse(form.is_valid())

class UtilsTests(TestCase):
    @patch('checker.utils.requests.get')
    def test_geocode_location_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"lat": "37.77", "lon": "-122.42"}]
        coords = geocode_location("San Francisco", "CA", "USA")
        self.assertEqual(coords, (37.77, -122.42))

    @patch('checker.utils.requests.get')
    def test_geocode_location_failure(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        coords = geocode_location("FakeCity", "FakeState", "FakeCountry")
        self.assertIsNone(coords)

    @patch('checker.utils.requests.get')
    def test_fetch_air_quality_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"hourly": {"us_aqi": [50], "time": ["2025-06-16T00:00"]}}
        data = fetch_air_quality(37.77, -122.42)
        self.assertIn("hourly", data)

    @patch('checker.utils.requests.get')
    def test_fetch_air_quality_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")
        data = fetch_air_quality(0, 0)
        self.assertIsNone(data)

class IntegrationTests(TestCase):
    @patch('checker.utils.geocode_location')
    @patch('checker.utils.fetch_air_quality')
    def test_location_view_success(self, mock_fetch, mock_geocode):
        mock_geocode.return_value = (37.77, -122.42)
        mock_fetch.return_value = {
            "hourly": {
                "us_aqi": [32],
                "time": ["2025-06-20T18:00"],
                "pm2_5": [None],
                "pm10": [None],
                "ozone": [None]
            }
        }
        client = Client()
        response = client.post(reverse('location_form'), {
            "city": "San Francisco",
            "state": "CA",
            "country": "USA"
        })
        self.assertContains(response, ">AQI (US):</strong> 32<")

    @patch('checker.utils.geocode_location')
    def test_location_view_location_not_found(self, mock_geocode):
        mock_geocode.return_value = None
        client = Client()
        response = client.post(reverse('location_form'), {
            "city": "FakeCity",
            "state": "FakeState",
            "country": "FakeCountry"
        })
        self.assertContains(response, "Location not found")

    @patch('checker.views.geocode_location')
    @patch('checker.views.fetch_air_quality')
    def test_location_view_no_aqi_data(self, mock_fetch, mock_geocode):
        mock_geocode.return_value = (37.77, -122.42)
        mock_fetch.return_value = {"hourly": {"us_aqi": [None], "time": ["2025-06-20T18:00"]}}
        client = Client()
        response = client.post(reverse('location_form'), {
            "city": "San Francisco",
            "state": "CA",
            "country": "USA"
        })
        self.assertContains(response, "No recent air quality data available.")
