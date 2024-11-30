from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.conf import settings

class EcomSettingsTests(TestCase):
    def test_debug_setting(self):
        """Ensure DEBUG setting is True for development."""
        self.assertTrue(settings.DEBUG)

    def test_installed_apps(self):
        """Verify core apps are installed."""
        required_apps = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.staticfiles",
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_custom_apps(self):
        """Verify custom apps are installed."""
        custom_apps = ["store.apps.StoreConfig", "cart.apps.CartConfig", "payment.apps.PaymentConfig"]
        for app in custom_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_static_and_media_settings(self):
        """Check STATIC_URL and MEDIA_URL settings."""
        self.assertEqual(settings.STATIC_URL, "/static/")
        self.assertEqual(settings.MEDIA_URL, "/media/")

class EcomURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_root_url_resolves(self):
        """Test that the root URL resolves to the store app."""
        resolver = resolve("/")
        self.assertEqual(resolver.app_name, "store")

    def test_cart_url_resolves(self):
        """Test that the cart URL resolves correctly."""
        resolver = resolve("/cart/")
        self.assertEqual(resolver.app_name, "cart")

    def test_payment_url_resolves(self):
        """Test that the payment URL resolves correctly."""
        resolver = resolve("/payment/")
        self.assertEqual(resolver.app_name, "payment")

    def test_admin_url(self):
        """Ensure the admin URL is accessible."""
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

class MiddlewareTests(TestCase):
    def test_middleware_classes(self):
        """Ensure essential middleware is configured."""
        required_middleware = [
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ]
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE)
