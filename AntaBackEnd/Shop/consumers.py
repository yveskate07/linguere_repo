import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.db.models import QuerySet
from Users.models import Fab_User
from .models import Order, Product
from asgiref.sync import sync_to_async

from .services.cart_service import CartService


class ProductConsumerAuth(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'msg': 'success'}))

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    @sync_to_async
    def get_sorted_products(self, order, from_filters=True, qs_to_filter=None):

        main_category = \
        {'installation': 'Installations Fablab', 'machine': 'Machines Numériques', 'arduino': 'Kits Arduino et IOT'}[
            order.get('main_category', 'arduino')]

        if order['sort'] not in ['asc', 'desc']:
            queryset = Product.objects.filter(main_category=main_category)
        else:
            queryset = Product.objects.filter(main_category=main_category).order_by(
                'price' if order['sort'] == 'asc' else '-price')

        if from_filters:
            return self.products_queryset(queryset, main_category=main_category)
        else:
            return queryset

    @sync_to_async
    def get_filtered_products(self, filters, from_filters=True, qs_to_sort=None):

        main_category = \
            {'installation': 'Installations Fablab', 'machine': 'Machines Numériques', 'arduino': 'Kits Arduino et IOT'}[
                filters.get('main_category', 'arduino')]

        qs = Product.objects.filter(main_category=main_category)

        categories = filters.get('categories', [])
        disponibility = filters.get('disponibility', [])
        price_range = filters.get('price_range', [0, 9999999])
        price_range = [int(i) for i in price_range]

        if categories:
            qs = qs.filter(category__in=categories)

        if not (price_range == [0,0] or price_range[0] > price_range[1]): # si le prix est valide
            if int(price_range[1]) > 0: # si le prix max est superieur a 0
                qs = qs.filter(price__gte=price_range[0], price__lte=price_range[1])
            else:
                qs = qs.filter(price__gte=price_range[0])
            print('Les prix sont valides')
        else:
            print('les prix sont invalides')

        if disponibility:
            qs = qs.filter(disponibility__in=disponibility)

        if from_filters:
            return self.products_queryset(qs, main_category=main_category)
        else:
            return qs


    @sync_to_async
    def add_to_cart(self, prd_data):

        prd_id = prd_data.get('id')
        quantity = prd_data.get('quantity', 0)
        uuid = self.scope['url_route']['kwargs']['uuid']

        if uuid != 'anonymous_id':
            # si l'utilisateur est authentifié, on ajoute l'item au panier de l'utilisateur
            user = Fab_User.objects.get(uuid=uuid)
            cart = CartService.get_cart(user)
        else:
            return 'user not authenticated'

        total_price = CartService.add_item(cart, product=prd_id, quantity=quantity)

        # user = Fab_User.objects.get(uuid=uuid)
        # cart = user.cart
        # item.quantity = quantity
        # if not item.cart:  # si l'item n'est pas encore dans le panier, on l'ajoute
        #     item.cart = cart
        #     msg = 'item added'
        # else:  # si l'item est deja dans le panier, on met a jour la quantite
        #     msg = 'already in cart'
        # item.save()
        #
        return total_price

    @sync_to_async
    def change_item_qtty(self, item_data):

        item_id = item_data.get('id', None)
        qtty = item_data.get('quantity', None)
        uuid = self.scope['url_route']['kwargs']['uuid']

        if uuid != 'anonymous_id':
            # si l'utilisateur est authentifié, on change la quantite du item dans le panier de l'utilisateur
            user = Fab_User.objects.get(uuid=uuid)
            cart = CartService.get_cart(user)
        else:
            return 'user not authenticated'

        response = CartService.update_quantity(cart, item_id=item_id, quantity=qtty)

        return response

    @sync_to_async
    def remove_item_from_cart(self, item_data):

        uuid = self.scope['url_route']['kwargs']['uuid']

        if uuid != 'anonymous_id':
            # si l'utilisateur est authentifié, on ajoute l'item au panier de l'utilisateur
            user = Fab_User.objects.get(uuid=uuid)
            cart = CartService.get_cart(user = user)
        else:
            return 'user not authenticated'

        response = CartService.remove_item(cart, item_id=item_data.get('item'))

        return response

    def product_to_dict(self, product, page=None): # transforms a product object into a dictionary

        return {
         'page': page,
         "id": product.id,
         "name": product.name,
         "price": str(product.price),  # convertir Decimal en str si nécessaire
         "main_category": product.main_category
        }

    def save_page_to_json(self, paginator): # given a paginator, saves each page of products to a json file
        if isinstance(paginator, Paginator):
            print(f'Nombre de pages: {paginator.num_pages}')
            for page_number in range(1, paginator.num_pages + 1):
                page = paginator.page(page_number)
                products_list = [self.product_to_dict(p, page_number) for p in page.object_list]
                filename = f"page{page.number}.json"

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(products_list, f, ensure_ascii=False, indent=4)

                print(f"Page {page_number} enregistrée dans {filename}")
        else:# if paginator is a single page of a paginator object
            products_list = [self.product_to_dict(p, 1) for p in paginator.object_list]
            filename = f"page{paginator.number}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products_list, f, ensure_ascii=False, indent=4)

            print(f"Page {paginator.number} enregistrée dans {filename}")

    def products_queryset(self, queryset, page_number=1, main_category=None):

        if not isinstance(queryset, QuerySet):
            queryset = Product.objects.filter(id__in=[p.id for p in queryset])  # reconvertir liste → queryset
        
        if not queryset.exists():
            queryset = Product.objects.filter(main_category=main_category)

        paginator = Paginator(queryset, 30)
        page = paginator.get_page(page_number)

        query_dict = {
            "items": list(page.object_list.values(
                "id", "name", "price", "category", "badge", "disponibility", "stock", "description", "image"
            )),
            "has_previous": page.has_previous(),
            "previous_page_number": page.previous_page_number() if page.has_previous() else None,
            "number": page.number,
            "num_pages": paginator.num_pages,
            "has_next": page.has_next(),
            "next_page_number": page.next_page_number() if page.has_next() else None,
        }

        return query_dict
    
    @sync_to_async
    def product_page(self, page_number, filters=None, sort=None, page_range=None):
        if filters is not None:
            main_category = \
            {'installation': 'Installations Fablab', 'machine': 'Machines Numériques', 'arduino': 'Kits Arduino et IOT'}[
                filters.get('main_category', 'arduino')]

            qs = Product.objects.filter(main_category=main_category)

            categories = filters.get('categories', [])
            disponibility = filters.get('disponibility', [])
            price_range = filters.get('price_range', [0, 9999999])
            price_range = [int(i) for i in price_range]

            if categories:
                qs = qs.filter(category__in=categories)

            if not (price_range == [0,0] or price_range[0] > price_range[1]): # si le prix est valide
                if int(price_range[1]) > 0: # si le prix max est superieur a 0
                    qs = qs.filter(price__gte=price_range[0], price__lte=price_range[1])
                else:
                    qs = qs.filter(price__gte=price_range[0])
                print('Les prix sont valides')
            else:
                print('les prix sont invalides')

            if disponibility:
                qs = qs.filter(disponibility__in=disponibility)

        if sort is not None:
            main_category = \
            {'installation': 'Installations Fablab', 'machine': 'Machines Numériques', 'arduino': 'Kits Arduino et IOT'}[
                filters.get('main_category', 'arduino')]

            if sort not in ['asc', 'desc']:
                qs = Product.objects.filter(main_category=main_category)
            else:
                qs = Product.objects.filter(main_category=main_category).order_by(
                    'price' if sort == 'asc' else '-price')
                
        elif not filters and not sort:
            print("Aucun filtre ou tri")
            qs = Product.objects.all()

        paginator = Paginator(qs, 30)
        page = paginator.get_page(page_number)

        self.save_page_to_json(paginator=paginator)

        # Calcul des pages à afficher
        #print('Nombre de pages du paginator: ',paginator.num_pages)
        if paginator.num_pages <= 3:
            #print('paginator a 3 pages ou moins')
            # Si peu de pages, on les affiche toutes
            page_range = paginator.page_range
        else:
            #print('paginator a plus de 3 pages')
            if page.number == 1:
                start_page = 1
            elif page.number == paginator.num_pages:
                start_page = paginator.num_pages - 2
            else:
                start_page = page.number - 1

            end_page = start_page + 2
            page_range = range(start_page, min(end_page, paginator.num_pages) + 1)

        #print(f"page range is : {list(page_range)}")

        query_dict = {
            "items": list(page.object_list.values(
                "id", "name", "price", "category", "badge", "disponibility", "stock", "description", "image"
            )),
            "has_previous": page.has_previous(),
            "previous_page_number": page.previous_page_number() if page.has_previous() else None,
            "number": page_number,
            "num_pages": paginator.num_pages,
            "has_next": page.has_next(),
            "page_range":list(page_range),
            "next_page_number": page.next_page_number() if page.has_next() else None,
        }

        print("query_dict:", {"has_previous": page.has_previous(),
            "previous_page_number": page.previous_page_number() if page.has_previous() else None,
            "number": page_number,
            "num_pages": paginator.num_pages,
            "has_next": page.has_next(),
            "page_range":list(page_range),
            "next_page_number": page.next_page_number() if page.has_next() else None})

        return query_dict

    @sync_to_async
    def get_order_datas(self, text_data=None):
        # Assuming the user is authenticated and has a cart
        uuid = self.scope['url_route']['kwargs']['uuid']
        
        if uuid != 'anonymous_id':
            user = Fab_User.objects.get(uuid=uuid)
        else: # user not authenticated
            return 'user not authenticated'

        # getting an order
        order = Order.objects.get(user=user, complete=False, transaction_id=text_data.get('transaction_id'))

        return {'total_price': order.total_amount, 'transaction_id': order.transaction_id,
                'ref_commande': f'Commande No: {order.id}', 'client_name': user.first_name + ' ' + user.last_name}
    
    @sync_to_async
    def create_new_order(self):
        uuid = self.scope['url_route']['kwargs']['uuid']
        
        if uuid != 'anonymous_id':
            user = Fab_User.objects.get(uuid=uuid)
            cart = CartService.get_cart(user)
        else:
            return 'user not authenticated'
        
        total_price = CartService.get_total_price(cart)

        # creating a new order
        order = Order.objects.create(user=user, total_amount=total_price, complete=False)

        return {'total_price': total_price, 'transaction_id': order.transaction_id,
                'ref_commande': f'Commande No: {order.id}', 'client_name': user.first_name + ' ' + user.last_name}


    @sync_to_async
    def saving_pre_payment_data(self, text_data):
        order_datas = text_data.get('datas', {})
        
        uuid = self.scope['url_route']['kwargs']['uuid']

        if uuid != 'anonymous_id':
            user = Fab_User.objects.get(uuid=uuid)
            
            order = Order.objects.get(transaction_id=order_datas.get('transactionId'))
            user.first_name = order_datas.get('first-name', user.first_name)
            user.last_name = order_datas.get('last-name', user.last_name)
            user.email = order_datas.get('email', user.email)
            user.adress = order_datas.get('address', user.adress)
            user.phone_number = order_datas.get('payment-phone', user.phone_number)

            user.save()

            order.user = user

            order.payment_method = order_datas.get('paymentMethod', order.payment_method)

            order.save()

            return 'success'
            
        else: # renvoyer le client vers la page de connexion
            return 'user not authenticated'

    @sync_to_async
    def confirm_payment_order(self, text_data=None):
        order_datas = text_data.get('datas', {})
        uuid = self.scope['url_route']['kwargs']['uuid']

        if uuid != 'anonymous_id':
            try:
                user = Fab_User.objects.get(uuid=uuid)
            except:
                user = self.scope['user']
            
            cart = CartService.get_cart(user)

            order = Order.objects.get(transaction_id=order_datas.get('transactionId'), complete=False)
            order.complete = True

            order.save()

            to_email = user.email

            # envoi de mail au client pour confirmer la commande
            order.send_confirmation(
                text_content="Votre commande a été confirmée.",
                template_name='Shop/mail_templates/users/index.html',
                context={'numero_commande':order.id, 'first_name':order.user.first_name,
                        'second_name':order.user.last_name,
                        'adresse_livraison':order.user.adress,
                        'telephone':order.user.phone_number,
                        'mode_paiement':order.payment_method,
                        'statut':order.status,
                        'date_commande':order.date,
                        'frais_livraison':order.delivery_price,
                        'total':order.total_amount},
                subject=f'Confirmation de la commande {order.id}',
                to_email=to_email
            )

            # envoi de mail a l'admin pour confirmer la commande
            order.send_confirmation(
                text_content="Une nouvelle commande a été passée.",
                template_name='Shop/mail_templates/fablab/index.html',
                context={'numero_commande':order.id,
                        'first_name':order.user.first_name,
                        'second_name':order.user.last_name,
                        'adresse_livraison':order.user.adress,
                        'telephone':order.user.phone_number,
                        'email':to_email,
                        'mode_paiement':order.payment_method,
                        'statut':order.status,
                        'date_commande':order.date,
                        'frais_livraison':order.delivery_price,
                        'total':order.total_amount,
                        'order_id': order.id,
                        "admin_link": order.admin_link},
                subject=f'Nouvelle commande {order.id}',
                to_email=to_email
            )

            CartService.clear_cart(cart)

    async def receive(self, text_data):

        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "sort": # sort products
            products = await self.get_sorted_products(data)
            await self.send(text_data=json.dumps({'products': products['items'],'pagination': {
            "has_previous": products["has_previous"],
            "previous_page_number": products["previous_page_number"],
            "number": products["number"],
            "num_pages": products["num_pages"],
            "has_next": products["has_next"],
            "next_page_number": products["next_page_number"],
        }, 'type': 'display_products', 'length':len(products['items'])}))
        elif message_type == "filter": # filter products
            filters = data.get("filters", {})
            products = await self.get_filtered_products(filters)
            await self.send(text_data=json.dumps({'products': products['items'],
            'pagination': {
            "has_previous": products["has_previous"],
            "previous_page_number": products["previous_page_number"],
            "number": products["number"],
            "num_pages": products["num_pages"],
            "has_next": products["has_next"],
            "next_page_number": products["next_page_number"],
        }, 
        'type': 'display_products', 'length':len(products['items'])}))
        elif message_type == "add-to-cart": # add item to cart
            response = await self.add_to_cart(data.get('item', {}))
            if response == 'user not authenticated':
                await self.send(text_data=json.dumps({'type': 'user_not_authenticated'}))
                return
            await self.send(text_data=json.dumps({'type': 'add_to_cart_result', "total_price": response}))
            return
        elif message_type == "change-item-quantity": # change item quantity in cart
            response = await self.change_item_qtty(data.get('item', {}))
            if response == 'does not exist':
                return
            elif response[0] == 'deleted':
                await self.send(text_data=json.dumps({'type': 'remove_item_result', "html_id": data.get('item').get('html_id'), "total_price": response[1]}))
                return
            await self.send(text_data=json.dumps({'type': 'quantity_changed', 
                                                  "new_qtty": response[0], 
                                                  "new_total": response[1], 
                                                  'item_qtty' : response[2], 
                                                  'item_name': response[3], 
                                                  'item_total': response[4]}))
            return
        elif message_type == "remove-item": # remove item from cart
            msg = await self.remove_item_from_cart(data)
            if msg == 'user not authenticated':
                await self.send(text_data=json.dumps({'type': 'user_not_authenticated'}))
                return
            await self.send(text_data=json.dumps(
                {'type': 'remove_item_result', "status": "success", 'total_price': msg, 'html_id': data.get('html_id')}))
            return
        
        elif message_type == "get_order_datas": # get order total price, transaction_id, ref_commande, client_name before payment then display payment modal in front end
            datas = await self.get_order_datas()
            if datas == 'user not authenticated':
                await self.send(text_data=json.dumps({'type': 'user_not_authenticated'}))
                return
            await self.send(text_data=json.dumps({'type': 'order_datas', 'total_price': datas['total_price'],
                                                  'transaction_id': datas['transaction_id'],
                                                  'ref_commande':datas['ref_commande'],
                                                  'client_name': datas['client_name']}))
            return
        
        elif message_type == "create_new_order": # create a new order when the user clicks on the payment button
            datas = await self.create_new_order()
            if datas == 'user not authenticated':
                await self.send(text_data=json.dumps({'type': 'user_not_authenticated'}))
                return
            await self.send(text_data=json.dumps({'type': 'order_created', 'total_price': datas['total_price'],
                                                    'transaction_id': datas['transaction_id'],
                                                    'ref_commande':datas['ref_commande'],
                                                    'client_name': datas['client_name']}))

        elif message_type == "prepayment_datas": # receive prepayment datas from front end and save them in the order
            response = await self.saving_pre_payment_data(data)
            if response == 'user not authenticated':
                await self.send(text_data=json.dumps({'type': 'user_not_authenticated'}))
                return
            await self.send(text_data=json.dumps({'type': 'process_payment', 'paymentMethod': data.get('datas', {}).get('paymentMethod', 'WAVE')}))
            return
        
        elif message_type == "payment_achieved":
            response = await self.confirm_payment_order(data)
            await self.send(text_data=json.dumps({'type': 'payment_confirmed'}))

        elif message_type == "product_page":
            page_number = data.get('page_number', 1)
            page_range=data.get('list_page_range', None)
            print(f'Vous avez demandé page : {page_number}2\n page range: {page_range}')
            products = await self.product_page(page_number, filters=data.get('filters', None), sort=data.get('sort', None), page_range=page_range)
            await self.send(text_data=json.dumps({'products': products['items'],'pagination': {
            "has_previous": products["has_previous"],
            "previous_page_number": products["previous_page_number"],
            "number": products["number"],
            "num_pages": products["num_pages"],
            "has_next": products["has_next"],
            "next_page_number": products["next_page_number"],
            "page_range":list(products['page_range']),
        }, 'type': 'display_products', 'length':len(products['items'])}))
            return