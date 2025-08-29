import hashlib
import hmac
import json

import requests
from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from AntaBackEnd import settings
from Users.models import Fab_User
from .models import Product, Cart
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .services.cart_service import CartService


@csrf_exempt
def notify(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)  # Payment API usually sends JSON
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    # TODO: Verify payment API signature if provided
    # Example: compare a hash from headers with your secret
    # Process the notification data

@csrf_exempt
def init_payment(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            # Construire la payload complète pour CINETPAY avec tes clés sensibles cachées dans settings
            payload = {
                "apikey": settings.CINETPAY_API_KEY,
                "site_id": settings.CINETPAY_SITE_ID,
                "transaction_id": body.get("transaction_id"),
                "amount": body.get("amount"),
                "currency": "XOF",
                "notify_url": body.get('notify_url'),  # ton endpoint notify
                "return_url": body.get('return_url'),  # ton endpoint retour
                "channels": body.get("channels", "ALL"),
                "metadata": body.get("metadata"),
                "lang": "FR",
                "invoice_data": body.get("invoice_data", {})
            }

            # Envoi de la requête POST à CINETPAY
            response = requests.post("https://api-checkout.cinetpay.com/v2/payment", json=payload)

            # On retourne la réponse telle quelle au client
            return JsonResponse(response.json(), status=response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def verify_hmac(request):
    if request.method == "POST":
        try:
            # Récupérer les données de la notification
            data = request.POST
            signature = data.get("signature")

            # Créer la chaîne à signer
            message = f"{data.get('cpm_site_id')}{data.get('cpm_trans_id')}{data.get('cpm_amount')}{data.get('cpm_currency')}{data.get('cpm_custom')}{data.get('cpm_payment_date')}"

            # Calculer le HMAC avec la clé secrète
            secret_key = settings.CINETPAY_SECRET_KEY.encode()
            calculated_signature = hmac.new(secret_key, message.encode(), hashlib.sha256).hexdigest()

            # Comparer les signatures
            if hmac.compare_digest(calculated_signature, signature):
                # Vérifier le statut de la transaction
                transaction_id = data.get("cpm_trans_id")
                verification_response = verify_transaction(transaction_id)

                if verification_response.get("code") == "00" and verification_response.get("data", {}).get(
                        "status") == "ACCEPTED":
                    # Traiter la commande
                    return JsonResponse({"status": "success", "message": "Paiement validé"})
                else:
                    return JsonResponse({"status": "error", "message": "Paiement échoué"}, status=400)
            else:
                return JsonResponse({"status": "error", "message": "Signature invalide"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def verify_transaction(transaction_id):
    payload = {
        "apikey": settings.CINETPAY_API_KEY,
        "site_id": settings.CINETPAY_SITE_ID,
        "transaction_id": transaction_id
    }

    response = requests.post("https://api-checkout.cinetpay.com/v2/payment/check", json=payload)
    return response.json()

def return_url(request):
    transaction_id = request.POST.get("transaction_id")
    # Vérifier le statut de la transaction
    verification_response = verify_transaction(transaction_id)

    if verification_response.get("code") == "00" and verification_response.get("data", {}).get("status") == "ACCEPTED":
        return JsonResponse({"status": "success", "message": "Paiement réussi"})
    else:
        return JsonResponse({"status": "error", "message": "Paiement échoué"}, status=400)


def render_category_page(request, page_number, category, template):
    products = Product.objects.filter(main_category=category)
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
    products_cart = CartService.get_cart_data_from_request(request)
    context = {
        'user_authenticated': user_authenticated,
        'user_id': user_id,
        'user': user,
        'products': page,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
        "page_range": list(page_range)
    }

    return render(request, template, context)

def arduino(request):
    return render_category_page(request, category="Kits Arduino et IOT", template='Shop/arduino/index.html', page_number=1)

def installations(request):
    return render_category_page(request, category="Installations Fablab", template="Shop/installations/index.html", page_number=1)

def machine(request):
    return render_category_page(request, category="Machines Numériques", template="Shop/machine/index.html", page_number=1)