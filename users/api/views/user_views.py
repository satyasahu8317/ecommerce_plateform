from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from cart.cart import CartManager

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            cart = CartManager(request)
            cart.merge_session_cart()

        return response