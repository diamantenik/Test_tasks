from django.test import TestCase, Client
from django.urls import reverse

class WeatherTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_stats_api_returns_json(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
