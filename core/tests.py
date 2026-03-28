from django.test import TestCase
from django.urls import reverse


class HomePageViewTests(TestCase):
    def test_home_page_returns_success(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home-page.html')
