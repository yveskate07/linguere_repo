from .models import Cart


def get_cart_data(request):
    total_price_cart = 0
    total_products_cart = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_price_cart = cart.total_price
            total_products_cart = cart.total_items

        except Cart.DoesNotExist:
            total_price_cart = 0
            total_products_cart = 0

    return dict(
        total_price_cart=total_price_cart,
        total_products_cart=total_products_cart,
    )
