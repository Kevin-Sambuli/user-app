from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import registration_view, profile_view, webMap, userProfiles


class TestUrls(SimpleTestCase):

    def test_registration_url_registration_view(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registration_view)

    # def test_map_url_registration_view(self):
    #     url = reverse('map')
    #     self.assertEquals(resolve(url).func, webMap)
    #
    # def test_registration_url_registration_view(self):
    #     url = reverse('register', args=['some-detail'])
    #     self.assertEquals(resolve(url).func, registration_view)