class CartManager:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, variant_id=None):
        if self.user.is_authenticated:
            from .models import Cart, CartItem
            cart_obj, _ = Cart.objects.get_or_create(user=self.user)
            item, created = CartItem.objects.get_or_create(
                cart = cart_obj,
                product_id = product_id,
                variant_id = variant_id
            )
            if not created:
                item.quantity += quantity
                item.save()
        else:
            item_id = f"{product_id}_{variant_id}" if variant_id else str(product_id)
            if item_id not in self.cart:
                self.cart[item_id] = {'quantity': 0, 'variant_id': variant_id}
            self.cart[item_id]['quantity'] += quantity
            self.session.modified = True
