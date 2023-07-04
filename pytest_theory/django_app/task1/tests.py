from django.test import TestCase


class URLTest(TestCase):
    def test_homepage(self):
        response = self.client.get("/")
        print("Hello from first home page test! Hope all other tests will be successful")
        self.assertEqual(response.status_code, 302)

