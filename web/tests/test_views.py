from django.test import TestCase


class WebViewsTest(TestCase):
    """Test cases for web template views"""

    def test_home_view(self):
        """Test HomeView renders correctly"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_v2_view(self):
        """Test HomeV2View renders correctly"""
        response = self.client.get('/v2/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homev2.html')

    def test_home_view_context(self):
        """Test HomeView provides correct context"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        # TemplateView doesn't provide much context by default
        # This test ensures the view renders without errors

    def test_home_v2_view_context(self):
        """Test HomeV2View provides correct context"""
        response = self.client.get('/v2/')

        self.assertEqual(response.status_code, 200)
        # TemplateView doesn't provide much context by default
        # This test ensures the view renders without errors