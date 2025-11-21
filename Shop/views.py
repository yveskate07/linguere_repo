import hashlib
import hmac
import json
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from django.conf import settings
from Users.models import Fab_User
from .models import Payment, Product, Order
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .services.cart_service import CartService

def render_category_page(request, page_number, category, template, fetch_articles=None):
    print('render_category_page called with fetch_articles=', fetch_articles)
    if not fetch_articles:
        products = Product.objects.filter(main_category=category)
        print('No filters applied, total products:', products.count())
    else:
        products = Product.objects.filter(category__in=fetch_articles['categories']).filter(disponibility__in=fetch_articles['stocks'])
        print(f"Products count after filtering: {products.count()}")
        if fetch_articles['prices'][1]>0:
            products = products.filter(price__gte=fetch_articles['prices'][0], price__lte=fetch_articles['prices'][1])
            print(f"Products count after price filtering: {products.count()}")
        if fetch_articles['sort'] in ['asc', 'desc']:
            products = products.order_by('price' if fetch_articles['sort'] == 'asc' else '-price')
            print(f"Products ordered by price {fetch_articles['sort']}")
        
    paginator = Paginator(products, 30)
    page = paginator.get_page(page_number)
    user_authenticated = 'YES' if request.user.is_authenticated else 'No'

    if request.user.is_authenticated:
        user = get_object_or_404(Fab_User, uuid=request.user.uuid)
        user_id = user.uuid
    else:
        user = None
        user_id = 'anonymous_id'

    # Calcul des pages à afficher
    print('Nombre de pages du paginator: ',paginator.num_pages)
    if paginator.num_pages <= 3:
        print('paginator a 3 pages ou moins')
        # Si peu de pages, on les affiche toutes
        page_range = paginator.page_range
    else:
        print('paginator a plus de 3 pages')
        if page.number == 1:
            start_page = 1
        elif page.number == paginator.num_pages:
            start_page = paginator.num_pages - 2
        else:
            start_page = page.number - 1

        end_page = start_page + 2
        page_range = range(start_page, min(end_page, paginator.num_pages) + 1)

    print(f"page range is : {list(page_range)}")
    print('number of products in page: ', len(page.object_list))
    products_cart = CartService.get_cart_data_from_request(request)
    context = {
        'user_authenticated': user_authenticated,
        'user_id': user_id,
        'user': user,
        'products': page,
        'page_label': category,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
        "page_range": list(page_range)
    }

    return render(request, template, context)

@login_required
def arduino(request, page, fetch_articles=None):
    return render_category_page(request, category="Kits Arduino et IOT", template='Shop/arduino/index.html', page_number=page, fetch_articles=fetch_articles)

@login_required
def installations(request, page, fetch_articles=None):
    return render_category_page(request, category="Installations Fablab", template="Shop/installations/index.html", page_number=page, fetch_articles=fetch_articles)

@login_required
def machine(request, page, fetch_articles=None):
    return render_category_page(request, category="Machines Numériques", template="Shop/machine/index.html", page_number=page, fetch_articles=fetch_articles)

@login_required
def fetch_articles(request):
    print('method is ', request.method)
    if request.method == 'POST':
        filters = {'page':int(request.POST.get('page')), 
                   'sort':request.POST.get('sort-choice'),
                   'prices':[int(request.POST.get('min-price')), int(request.POST.get('max-price'))],
                   'stocks': request.POST.getlist('disponib-checks'),
                   'categories': request.POST.getlist('category-checks'),
                   'page-label': request.POST.get('page-label')}
        
        if filters['page-label'] == 'Kits Arduino et IOT':
            return arduino(request, page=filters['page'], fetch_articles=filters)
        elif filters['page-label'] == 'Installations Fablab':
            return installations(request, page=filters['page'], fetch_articles=filters)
        else:
            return machine(request, page=filters['page'], fetch_articles=filters)

@csrf_exempt
def init_payment(request):
    if request.method == "POST":
        user = request.user
        cart = user.cart
        try:
            body = json.loads(request.body)
            payment = Payment.objects.create(payment_method=body.get('metadata'), total_amount=int(body.get("amount")))
            # Construire la payload complète pour CINETPAY avec tes clés sensibles cachées dans settings
            payload = {
                "apikey": settings.CINETPAY_API_KEY,
                "site_id": settings.CINETPAY_SITE_ID,
                "transaction_id": payment.transaction_id,
                "amount": cart.total_price, # doit etre un multiple de 5
                "currency": "XOF",
                "metadata": user.id,
                "notify_url": body.get('notify_url'),  # endpoint notify
                "return_url": body.get('return_url'),  # endpoint retour
                "channels": body.get("channels", "ALL"),
                "lang": "FR",
                "invoice_data": {
                    "Id Client": user.id,
                    "Moyen de paiement": body.get("metadata"),
                    "Montant payé": payment.total_amount + " CFA"
                    }
            }

            # Envoi de la requête POST à CINETPAY
            response = requests.post("https://api-checkout.cinetpay.com/v2/payment", json=payload)
            payment.payment_token = response.json().get("data", {}).get("payment_token", "")
            payment.save()
            # On retourne la réponse telle quelle au client
            return JsonResponse(response.json(), status=response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def verify_transaction(transaction_id):
    payload = {
        "apikey": settings.CINETPAY_API_KEY,
        "site_id": settings.CINETPAY_SITE_ID,
        "transaction_id": transaction_id
    }

    response = requests.post("https://api-checkout.cinetpay.com/v2/payment/check", json=payload, timeout=20)
    return response.json()

def verify_hmac(request): # vue qui recevra les notifications de CinetPay
    if request.method != "POST":
        # La doc recommande que l’URL soit dispo en GET/POST, mais le POST contient les data.
        return HttpResponse(status=405)

    # 1) Récupérer le HMAC envoyé par CinetPay dans le header `x-token`
    received_token = request.headers.get("x-token") or request.META.get("HTTP_X_TOKEN", "")
    data = request.POST  # x-www-form-urlencoded selon la doc


    # 2) Construire la chaîne à signer dans l’ORDRE EXACT défini par CinetPay
    fields_in_order = [
        "cpm_site_id",
        "cpm_trans_id",
        "cpm_trans_date",
        "cpm_amount",
        "cpm_currency",
        "signature",
        "payment_method",
        "cel_phone_num",
        "cpm_phone_prefixe",
        "cpm_language",
        "cpm_version",
        "cpm_payment_config",
        "cpm_page_action",
        "cpm_custom",
        "cpm_designation",
        "cpm_error_message",
    ]

    message = "".join((data.get(k, "") or "") for k in fields_in_order)

    # 3) Calculer le HMAC attendu (SHA256) avec ta Secret Key
    secret_key = settings.CINETPAY_SECRET_KEY.encode("utf-8")
    generated_token = hmac.new(secret_key, message.encode("utf-8"), hashlib.sha256).hexdigest()

    # 4) Comparer de manière sûre
    if not hmac.compare_digest(generated_token, (received_token or "").strip()):
        # On répond quand même 200 pour éviter des retries infinis, mais on loggue l’erreur côté serveur
        return JsonResponse({"status": "error", "reason": "invalid_hmac"}, status=200)

    # 5) HMAC OK → vérifier officiellement la transaction via /payment/check
    transaction_id = data.get("cpm_trans_id", "")

    if not transaction_id:
        return JsonResponse({"status": "error", "reason": "missing_transaction_id"}, status=400)

    check = verify_transaction(transaction_id)

    # 6) Traiter selon la réponse officielle
    is_paid = check.get("code") == "00" and check.get("data", {}).get("status") == "ACCEPTED"
    if is_paid:
        # TODO: marquer la commande comme payée, idempotent (si déjà traité, ne rien refaire)
        user = Fab_User.objects.get(id=data.get('cpm_custom'))
        order = Order.objects.create(user=user, complete=True, status="Expédiée")
        Payment.objects.filter(transaction_id=transaction_id).update(done=True, order=order)
        return JsonResponse({"status": "success"}, status=200)
    else:
        # REFUSED / PENDING / autre: on enregistre l’état mais on n’échoue pas le webhook
        return JsonResponse(
            {
                "status": "not_accepted",
                "code": check.get("code"),
                "cp_status": check.get("data", {}).get("status"),
            },
            status=200,
        )

def return_url(request):
    transaction_id = request.POST.get("transaction_id")
    # Vérifier le statut de la transaction
    verification_response = verify_transaction(transaction_id)

    if verification_response.get("code") == "00" and verification_response.get("data", {}).get("status") == "ACCEPTED":
        messages.success(request, "Votre paiement a été effectué avec succès ✅")
        return redirect('payment-done')
    else:
        return JsonResponse({"status": "error", "message": "Paiement échoué"}, status=400)

@login_required
def cart_view(request):
    products_cart = CartService.get_cart_data_from_request(request)
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request,'cart/index.html', context={
        'products_cart': products_cart['products'],
        'user_id': user_id,
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})

def payment_done(request):
    if request.method == "POST":
        return render(request, 'Shop/payment_done/index.html')
    else:
        return redirect('home')