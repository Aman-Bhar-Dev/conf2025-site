from django.test import TestCase
from django.urls import reverse

class ItineraryPageTests(TestCase):
    def test_itinerary_page_status_code(self):
        response = self.client.get(reverse('itinerary'))
        self.assertEqual(response.status_code, 200)

    def test_itinerary_uses_correct_template(self):
        response = self.client.get(reverse('itinerary'))
        self.assertTemplateUsed(response, 'conference/itinerary.html')
