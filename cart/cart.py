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

    def merge_session_cart(self):
        session_cart = self.session.get('cart',{})
        for item_id, details in session_cart.items():
            parts = item_id.split('_')
            p_id = parts[0]
            v_id = parts[1] if len(parts)> 1 else None
            self.add(
                product_id = p_id,
                quantity=details['quantity'],
                variant_id=v_id
            )

        self.session['cart'] = {}
        self.session.modified = True

    def get_total_items(self):
        if self.user.is_authenticated:
            from .models import Cart
            cart_obj, _ = Cart.objects.get_or_create(user=self.user)
            return cart_obj.items.select_related('product','variant').all()
        return self.cart

    def remove(self, product_id, variant_id=None):
        # Removes a specific item from the cart
        if self.user.is_authenticated:
            from .models import Cart, CartItem
            try:
                cart_obj=Cart.objects.get(user=self.user)
                CartItem.objects.filter(
                    cart=cart_obj,
                    product_id=product_id,
                    variant_id=variant_id).delete()
            except Cart.DoesNotExist:
                pass    
        else:
            item_id = f"{product_id}_{variant_id}" if variant_id else str(product_id)
            if item_id in self.cart:
                del self.cart[item_id]
                self.session.modified = True

    def update_quantity(self, product_id, quantity, variant_id=None):
        if self.user.is_authenticated:
            from .models import Cart, CartItem
            try:
                cart_obj = Cart.objects.get(user=self.user)
                item = CartItem.objects.get(
                    cart=cart_obj,
                    product_id=product_id,
                    variant_id=variant_id
                )
                if quantity > 0:
                    item.quantity = quantity
                    item.save()
                else:
                    item.delete()
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                pass
        else:
            item_id = f"{product_id}_{variant_id}" if variant_id else str(product_id)
            if item_id in self.cart:
                if quantity > 0:
                    self.cart[item_id]['quantity'] = quantity
                else:
                    del self.cart[item_id]
                self.session.modified = True

    def get_total_price(self):
        """Calculates the combined price of everyone in the cart"""
        if self.user.is_authenticated:
            from .models import Cart
            cart_obj, _ = Cart.objects.get_or_create(user=self.user)
            return sum(item.get_total_price() for item in cart_obj.items.all())
        
        # For Session users, we have to look up the prices manually
        from products.models import Product, ProductVariant
        total = 0
        for item_id, details in self.cart.items():
            parts = item_id.split('_')
            p_id = parts[0]
            v_id = parts[1] if len(parts) > 1 else None
            
            if v_id:
                price = ProductVariant.objects.get(id=v_id).price
            else:
                price = Product.objects.get(id=p_id).price
            
            total += price * details['quantity']
        return total

    def get_total_items(self):
        """Returns the total number of individual items in the cart"""
        if self.user.is_authenticated:
            from .models import Cart
            cart_obj, _ = Cart.objects.get_or_create(user=self.user)
            # pyrefly: ignore [missing-import]
            from django.db import models
            return cart_obj.items.aggregate(total=models.Sum('quantity'))['total'] or 0
        
        return sum(item['quantity'] for item in self.cart.values())   

    def clear(self):
        if self.user.is_authenticated:
            from .models import Cart
            try:
                cart_obj = Cart.objects.get(user=self.user)
                cart_obj.items.all().delete()
            except Cart.DoesNotExist:
                pass
        else:
            self.cart = {}
            self.session.modified = True    