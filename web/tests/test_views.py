from django.test import TestCase

from transmitata.__version__ import VERSION


class WebViewsTest(TestCase):
    """Test cases for web template views"""

    def test_home_view(self):
        """Test HomeView renders correctly"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context_contains_version(self):
        """Test HomeView provides version in context"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['version'], VERSION)

    def test_home_view_displays_version(self):
        """Test HomeView displays version in the page"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'v{VERSION}')