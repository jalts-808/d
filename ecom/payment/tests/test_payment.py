from django.test import TestCase
from django.urls import reverse
from payment.forms import PaymentForm, ShippingForm
from payment.models import ShippingAddress, Order


class TestPaymentForms(TestCase):
    def test_valid_payment_form(self):
        data = {
            "card_name": "John Doe",
            "card_number": "1234123412341234",
            "card_expiry_date": "12/25",
            "card_ccv_number": "123",
            "card_address1": "123 Test Street",
            "card_city": "Test City",
            "card_state": "Test State",
            "card_postal_code": "12345",
            "card_country": "Test Country",
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_payment_form(self):
        data = {
            "card_name": "",
            "card_number": "invalid_number",
        }
        form = PaymentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_shipping_form(self):
        data = {
            "shipping_full_name": "John Doe",
            "shipping_email": "john@example.com",
            "shipping_address1": "123 Test Street",
            "shipping_city": "Test City",
            "shipping_state": "Test State",
            "shipping_postal_code": "12345",
            "shipping_country": "Test Country",
        }
        form = ShippingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_shipping_form(self):
        data = {
            "shipping_full_name": "",
            "shipping_email": "invalid_email",
        }
        form = ShippingForm(data=data)
        self.assertFalse(form.is_valid())


class TestPaymentModels(TestCase):
    def setUp(self):
        self.shipping = ShippingAddress.objects.create(
            shipping_full_name="John Doe",
            shipping_email="john@example.com",
            shipping_address1="123 Test Street",
            shipping_city="Test City",
            shipping_state="Test State",
            shipping_postal_code="12345",
            shipping_country="Test Country",
        )
        self.order = Order.objects.create(
            full_name="John Doe",
            email="john@example.com",
            shipping_address="123 Test Street, Test City, Test State",
            amount_paid=100.50,
        )

    def test_shipping_str(self):
        self.assertEqual(str(self.shipping), "Shipping Address - None")  # Update if `user` is set in tests

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order = {self.order.id}")


class TestPaymentViews(TestCase):
    def test_payment_success_view(self):
        response = self.client.get(reverse("payment-success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/payment_success.html")

    def test_checkout_view(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/checkout.html")
