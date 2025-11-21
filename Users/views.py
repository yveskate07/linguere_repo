import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_decode
from .auth_form import UserLoginForm, UserSignUpForm
from .tasks import send_verification_email
from Shop.services.cart_service import CartService
from .models import Fab_User

def check_user_activated(request):
    if not request.user.is_active:
        messages.error(request, "Votre compte n'est pas activé. Veuillez vérifier votre e-mail pour activer votre compte.")
        return render(request, 'Users/auths/login.html', {'form': UserLoginForm()})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = Fab_User.objects.get(username=username)
            except Fab_User.DoesNotExist:
                messages.error(request, "Cet utilisateur n'existe pas.")
                return render(request, 'Users/auths/login.html', context={'form': form})
            else:
                check_user_activated(request)
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'Users/auths/login.html', context={'form': form})
    else:
        messages.info(request, "Connectez-vous à votre compte en remplissant le formulaire ci-dessous.")
        return render(request, 'Users/auths/login.html', context={'form': UserLoginForm()})

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Fab_User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Fab_User.DoesNotExist):
        user = None

    if user.is_active:
        messages.info(request, "Votre compte est déjà activé. Veuillez vous connecter.")
        return redirect('login')

    # si l'utilisateur existe et que le token est valide
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitations ! Votre compte a été activé avec succès.')
        return redirect('home')
    else:
        messages.error(request, "Lien d'activation invalide !")
        return redirect('login')

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, "Vous êtes déjà connecté.")
        return redirect('home')
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            tel_num = form.cleaned_data.get('tel_num')
            adress = form.cleaned_data.get('adress')
            password = form.cleaned_data.get('password')

            user = Fab_User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                tel_num=tel_num,
                adress=adress,
                password=password,
            )

            user.save()
            print('RECEPTION DES DONNEES OK ! ENVOI DE MAIL...')

            # Send verification email
            mail_subject = 'Veuillez activer votre compte.'
            email_template = 'Users/emails/account_verification.html'
            protocol = 'https' if request.is_secure() else 'http'
            domain = get_current_site(request).domain

            send_verification_email.delay(protocol, domain, user.pk, mail_subject, email_template)
            print("APRES ENVOI DU MAIL !")


            messages.success(request, "Votre compte a été créé avec succès! Veuillez vérifier votre e-mail pour activer votre compte.")
            return redirect('login')
        else:
            return render(request, "Users/auths/signup.html", {'form': form})
    else:
        return render(request, 'Users/auths/signup.html', context={'form': UserSignUpForm()})



@login_required
def user_home(request):
    check_user_activated(request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    products_cart = CartService.get_cart_data_from_request(request)
    # si l'utilisateur est un superuser, rediriger vers la page d'administration
    if user.is_superuser:
        return redirect('/admin')
    return render(request ,'Users/home/index.html', {'user':user,
        
        'user_id': user_id,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],})

@login_required
def user_edit(request):
    check_user_activated(request)
    if request.method == "POST":
        user = get_object_or_404(Fab_User, uuid=request.user.uuid)
        user.tel_num = request.POST.get("tel_num")
        user.adress = request.POST.get("adress")
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.set_password(request.POST.get("password"))

        user.save()

    return redirect('user_home')

@login_required
def user_orders(request):
    check_user_activated(request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Users/orders/index.html", {'user':user,
        
        'user_id': user_id,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})

@login_required
def user_favourites(request):
    check_user_activated(request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Users/favourites/index.html", {'user':user,
        'user_id': user_id,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})

@login_required
def user_tracked_deliveries(request):
    check_user_activated(request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Users/tracked_deliveries/index.html", {'user':user,
        'user_id': user_id,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})
