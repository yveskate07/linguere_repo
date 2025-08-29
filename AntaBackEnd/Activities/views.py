import json

from django.shortcuts import render

from Shop.services.cart_service import CartService


# Create your views here.
def smart_coders(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for smart_coders requested
    """
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Activities/smart_coders/index.html", context={
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],})

def fab_elle(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_elle requested
    """
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Activities/fab_elle/index.html", context={
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],})

def fab_tour(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_tour requested
    """
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Activities/fab_tour/index.html", context={
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],})