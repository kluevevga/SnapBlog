from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.end_points = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

    def setUp(self):
        self.guest_client = Client()

    def test_status_code(self):
        for url in self.end_points.keys():
            with self.subTest(url=url):
                code = self.guest_client.get(url).status_code
                self.assertEqual(code, 200,
                                 (f'\nendpoint: {url}'
                                  f'\nexpected status code: 200'
                                  f'\nactual status code: {code}\n'))

    def test_templates(self):
        for url, template in self.end_points.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template,
                    (f'\nexpected template: {template} in:'
                     f'\nreceived templates: '
                     f'{[t.name for t in response.templates]}\n'))
