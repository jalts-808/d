import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product
from cart.cart import Cart


@pytest.mark.django_db
class TestCartViews:
    def setup_method(self):
        """Setup test data."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(name="Test Product", price=10.0)

    def test_cart_summary(self, client):
        """Test the cart summary view."""
        client.login(username="testuser", password="testpass")
        url = reverse("cart-summary")
        response = client.get(url)
        assert response.status_code == 200
        assert "cart/cart_summary.html" in [template.name for template in response.templates]

    def test_cart_add(self, client):
        """Test adding a product to the cart."""
        client.login(username="testuser", password="testpass")
        url = reverse("cart-add")
        response = client.post(url, {"product_id": self.product.id, "product_qty": 2, "action": "post"})
        assert response.status_code == 200
        assert response.json()["qty"] == 2  # Assuming the cart initially had 0 items

    def test_cart_delete(self, client):
        """Test deleting a product from the cart."""
        client.login(username="testuser", password="testpass")
        # Add product first
        cart = Cart(client)
        cart.add(product=self.product, quantity=2)
        url = reverse("cart-delete")
        response = client.post(url, {"product_id": self.product.id, "action": "post"})
        assert response.status_code == 200
        assert response.json()["product"] == self.product.id

    def test_cart_update(self, client):
        """Test updating a product quantity in the cart."""
        client.login(username="testuser", password="testpass")
        # Add product first
        cart = Cart(client)
        cart.add(product=self.product, quantity=1)
        url = reverse("cart-update")
        response = client.post(url, {"product_id": self.product.id, "product_qty": 5, "action": "post"})
        assert response.status_code == 200
        assert response.json()["qty"] == 5