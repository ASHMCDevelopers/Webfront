from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test import Client


class MeasureListingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_anonymous_user_is_redirected_to_login(self):
        url = reverse('vote_main')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)