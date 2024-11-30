from django.conf import settings
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from ecom.views import HomePageView  # Replace with your actual view class
from ecom.utils import calculate_discount  # Replace with your actual utility function


# Test cases for settings
class TestSettings(TestCase):
    def test_installed_apps(self):
        """Ensure required apps are installed"""
        self.assertIn('cart', settings.INSTALLED_APPS)  # Replace 'cart' with your app names
        self.assertIn('store', settings.INSTALLED_APPS)

    def test_debug_mode(self):
        """Ensure DEBUG mode is disabled in production"""
        self.assertFalse(settings.DEBUG)  # Assuming production defaults

    def test_middleware_inclusion(self):
        """Ensure necessary middleware is present"""
        self.assertIn('django.middleware.security.SecurityMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.middleware.common.CommonMiddleware', settings.MIDDLEWARE)


# Test cases for URL configuration
class TestURLs(SimpleTestCase):
    def test_home_url_resolves(self):
        """Ensure home URL resolves to the correct view"""
        url = reverse('home')  # Replace with the actual name of your home route
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_nonexistent_url(self):
        """Ensure non-existent URL returns 404"""
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)


# Test cases for middleware behavior
class TestMiddleware(TestCase):
    def setUp(self):
        self.client = Client()

    def test_security_headers(self):
        """Ensure SecurityMiddleware adds security headers"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Strict-Transport-Security', response.headers)

    def test_common_headers(self):
        """Ensure CommonMiddleware processes requests correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)


# Test cases for utility functions
class TestUtils(TestCase):
    def test_calculate_discount(self):
        """Test discount calculation utility"""
        result = calculate_discount(100, 20)  # Assuming 20% off $100
        self.assertEqual(result, 80)

    def test_calculate_discount_zero(self):
        """Ensure zero discount returns original amount"""
        result = calculate_discount(100, 0)
        self.assertEqual(result, 100)

    def test_calculate_discount_full(self):
        """Ensure 100% discount returns zero"""
        result = calculate_discount(100, 100)
        self.assertEqual(result, 0)

    def test_calculate_discount_negative(self):
        """Ensure negative discount raises an error"""
        with self.assertRaises(ValueError):
            calculate_discount(100, -10)


# Test cases for views
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        """Ensure home view returns status code 200 and uses correct template"""
        response = self.client.get(reverse('home'))  # Replace with the actual route name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')  # Replace with your actual template

    def test_home_view_content(self):
        """Ensure home view renders expected content"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<h1>Welcome to Ecom</h1>')  # Replace with your actual content


# Test cases for templates
class TestTemplates(TestCase):
    def test_home_template_content(self):
        """Ensure home template renders correct HTML"""
        response = self.client.get(reverse('home'))  # Replace with your actual route name
        self.assertContains(response, '<title>Home</title>')  # Replace with expected HTML

    def test_missing_template(self):
        """Ensure missing templates raise errors"""
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get('/missing-template/')  # Replace with a route that uses a missing template
