from store.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get("session_key")

        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # If product_id already in cart, do nothing or update?
        # Right now, we do nothing if it already exists:
        if product_id not in self.cart:
            self.cart[product_id] = product_qty

        self.session.modified = True

        # If user is logged in, update Profile's old_cart field
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        self.cart[product_id] = product_qty
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

        return self.cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            # value is the quantity
            product_id = int(key)
            for product in products:
                if product.id == product_id:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total

    def __len__(self):
        """Return the total quantity of items in the cart (sum of quantities)."""
        return sum(self.cart.values())

    def get_prods(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        return self.cart

    def db_add(self, product, quantity):
        """
        Possibly an unused method. 
        If you do need it, keep it consistent with add().
        """
        product_id = str(product)
        product_qty = int(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = product_qty

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))
