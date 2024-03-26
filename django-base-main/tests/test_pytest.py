import unittest
import pytest
import json
from django.test.client import RequestFactory


from pages import views, models

class TestSolarEvent(unittest.TestCase):

    def test_reading(self):
        solar_events = views.read_solar_events()
        self.assertEqual(len(solar_events), 7)
    
    @pytest.mark.django_db
    def test_loading_endpoint(self):
        rf = RequestFactory()
        req = rf.get('/pages/load_solar_events')
        response = views.load_solar_events(req)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"result": "ok"})

class TestRevision(unittest.TestCase):

    def test_to_revision_models(self):
        input_data = [
            { "timestamp": "2024-03-26T11:58:06.587403"},
            { "timestamp": "2023-01-01T01:00:00.123456"},
        ]

        article = "Sample Article"
        expected = [
            models.Revision(timestamp="2024-03-26", article=article),
            models.Revision(timestamp="2023-01-01", article=article),
        ]

        actual = views.to_revision_models(input_data, article)
        self.assertEqual(actual[0].timestamp, expected[0].timestamp)
        self.assertEqual(actual[1].timestamp, expected[1].timestamp)
        self.assertEqual(actual[0].article, expected[0].article)
        self.assertEqual(actual[1].article, expected[1].article)