from Shop.models import CartItem, Cart, Product

SESSION_CART_KEY = "cart"

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
    def remove_item(cart, item_id, user_authenticated=True):
        if user_authenticated:
            item = CartItem.objects.get(cart=cart, id=item_id)
            if item:
                item.delete()
            return cart.total_price
        else:
            del cart["products"][str(item_id)]
            cart["total_price"] = sum([cart["products"][key]['quantity']*cart["products"][key]['price'] for key in cart["products"].keys()])
            return cart, cart['total_price']

    @staticmethod
    def update_quantity(cart, item_id, quantity, user_authenticated=True):
        if user_authenticated:
            try:            
                item = CartItem.objects.get(cart=cart, id=item_id)
                if item.quantity + int(quantity) <= 0 :
                    item.delete() 
                    return {'deleted':True, "total_price":cart.total_price, "msg": "Votre article a été retiré du panier."}           
                else:
                    item.quantity += int(quantity)
                    item.save()
                    
                    return {"deleted":False, "total_price":cart.total_price, "item_quantity":item.quantity, "item_total_price":item.total_price, "msg": "La quantité de votre article a été mise à jour."}
            
            except CartItem.DoesNotExist:
                return 'does not exist'
            
        else:
            if str(item_id) in cart["products"]:
                new_quantity = cart["products"][str(item_id)]["quantity"] + int(quantity)
                if new_quantity <= 0:
                    del cart["products"][str(item_id)]
                    cart["total_price"] = sum([cart["products"][key]['quantity']*cart["products"][key]['price'] for key in cart["products"].keys()])
                    deleted = True
                    msg = "Votre article a été retiré du panier."
                else:
                    cart["products"][str(item_id)]["quantity"] = new_quantity
                    cart["total_price"] = sum([cart["products"][key]['quantity']*cart["products"][key]['price'] for key in cart["products"].keys()])
                    deleted = False
                    msg = "La quantité de votre article a été mise à jour."
            
                return {'deleted':deleted, 'msg':msg, "cart":cart, "total_price":cart['total_price'], "item_quantity":cart["products"][str(item_id)]["quantity"], "item_total_price":cart["products"][str(item_id)]["price"] * cart["products"][str(item_id)]["quantity"]}    
        
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
        return cart.to_dict # return cart data as {"products": [list of product dicts], "total_price": cart total price,}

    @staticmethod
    def get_session_cart(session): # cart is like session['cart'] = {"products":{"12": {"quantity": 2, "unit_price": 100}, "7": {"quantity": 1, "unit_price": 100}}, "total_price":total_amount}, keys are products ids
        
        return session.get(SESSION_CART_KEY, {"products": {}, "total_price": 0}) # should return same as get_cart_data but from session
    

    @staticmethod
    def return_cart_data(request):
        if request.user.is_authenticated:
            user = request.user
            cart_data = CartService.get_cart_data(user=user)
        
        else:
            cart_data = CartService.get_session_cart(request.session)
        
        return cart_data
        
    
    @staticmethod
    def save_session_cart(session, cart):
        total_price = sum([cart["products"][key]['quantity']*cart["products"][key]['price'] for key in cart["products"].keys()])
        session[SESSION_CART_KEY] = cart
        session.modified = True
        return session, total_price


    @staticmethod
    def add_to_cart_from_session(session, name, image_url, description, disponibility, stock, product_id, quantity=1, unit_price=None):
        cart = CartService.get_session_cart(session)
        product_id = str(product_id)

        if product_id in cart["products"]:
            cart["products"][product_id]["quantity"] += quantity
            cart["products"][product_id]["id"] = product_id
            cart["products"][product_id]["price"] = unit_price
            cart["products"][product_id]["total_price"] = cart["products"][product_id]["quantity"] * unit_price
            cart["products"][product_id]["name"] = name
            cart["products"][product_id]["image"] = image_url
            cart["products"][product_id]["description"] = description
            cart["products"][product_id]["disponibility"] = disponibility
            cart["products"][product_id]["stock"] = stock
        else:
            cart["products"][product_id] = {'id': product_id, 'name': name, 'image': image_url, 'description': description, 'disponibility': disponibility, 'stock': stock, "quantity": quantity, "price": unit_price, "total_price": quantity * unit_price}

        cart["total_price"] = sum([cart["products"][key]['quantity']*cart["products"][key]['price'] for key in cart["products"].keys()])
        
        session[SESSION_CART_KEY] = cart

        return session, cart["total_price"]
