from Shop.models import CartItem, Cart, Product


class CartService:
    @staticmethod
    def get_cart(user=None):
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            raise ValueError("User or guest required")
        return cart

    @staticmethod
    def add_item(cart, quantity=1, product=None):
        prod_obj = Product.objects.get(id=product)
        item, created = CartItem.objects.get_or_create(cart=cart, product=prod_obj)
        
        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()

        return item.cart.total_price

    @staticmethod
    def remove_item(cart, item_id):
        item = CartItem.objects.get(cart=cart, id=item_id)
        if item:
            item.delete()
        return item.cart.total_items, item.cart.total_price

    @staticmethod
    def update_quantity(cart, item_id, quantity):
        try:
            item = CartItem.objects.get(cart=cart, id=item_id)
            item.quantity += int(quantity)
            item.save()
                
            return item.cart.total_items, item.cart.total_price, item.quantity
        
        except CartItem.DoesNotExist:
            return 'does not exist'
        
    @staticmethod
    def get_total_price(cart):
        return cart.total_price

    @staticmethod
    def clear_cart(cart):
        try:
            cart.items.all().delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_cart_data(user=None):
        cart = CartService.get_cart(user=user)
        return cart.to_dict

    @staticmethod
    def get_cart_data_from_request(request):
        try:
            user = request.user
            cart_data = CartService.get_cart_data(user=user)
        except:
            return 'user not authenticated'
        finally:
            return cart_data