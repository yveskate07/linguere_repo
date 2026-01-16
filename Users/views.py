import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_decode
from Users.forms import UserResetPasswordForm
from .auth_form import UserLoginForm, UserSignUpForm
from .models import Fab_User
from django.contrib.auth import login, authenticate
from Shop.models import Cart, Product, CartItem


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Fab_User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Fab_User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Veuillez réinitialiser votre mot de passe.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Le lien de réinitialisation du mot de passe est invalide, veuillez en demander un nouveau.')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            pk = request.session.get('uid')
            user = Fab_User.objects.get(pk=pk)
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
            return redirect('login')
        else:
            messages.error(request, 'Erreur lors de la réinitialisation du mot de passe.')
            return render(request, 'Users/reset_password/index.html', {'form': UserResetPasswordForm(), 'errors': form.errors})

    return render(request, 'Users/reset_password/index.html', {'form': UserResetPasswordForm()})


def forgot_password(request):
    return redirect('login')
    if request.method == 'POST':
        email = request.POST['email']

        if Fab_User.objects.filter(email=email).exists():
            user = Fab_User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Modification de votre mot de passe.'
            email_template = 'Users/emails/reset_password_email.html'
            protocol = 'https' if request.is_secure() else 'http'
            domain = get_current_site(request).domain
            #send_verification_email.delay(protocol, domain, user.pk, mail_subject, email_template, user_name=user.first_name)
            #send_verification_email(protocol, domain, user.pk, mail_subject, email_template, user_name=user.first_name)
            messages.success(request, 'Le lien de réinitialisation du mot de passe a été envoyé à votre adresse e-mail.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'Users/forgot_password/index.html')

def check_user_activated(user, request):
    # Cas où l'utilisateur est None ou AnonymousUser
    if user is None:
        messages.error(
            request,
            "Votre compte n'est pas activé. Veuillez vérifier votre e-mail pour l'activer."
        )
        return render(request, 'Users/auths/login.html', {'form': UserLoginForm()})

    # Cas où l'utilisateur existe mais n'est pas activé
    else:
        if not user.is_active:
            messages.error(
            request,
            "Votre compte n'est pas activé. Veuillez vérifier votre e-mail pour l'activer."
            )
            return render(request, 'Users/auths/login.html', {'form': UserLoginForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # Vérification custom
        """response = #check_user_activated(user, request)
        if response:
            return response"""

        if user is not None:

            # Connexion
            login(request, user)
            # fusion des paniers si nécessaire ici
            user_cart = Cart.objects.get_or_create(user=user)
            session_cart = request.session.get('cart', None)
            if session_cart and session_cart.get('products', None):
                for item_id, item_data in session_cart.get('products', {}).items():
                    product = Product.objects.get(id=item_id)
                    if not user_cart[0].has_item(product.id):
                        CartItem.objects.create(cart=user_cart[0], product=product, quantity=item_data['quantity'])
                request.session['cart'] = {'products': {}, 'total_price': 0}

            messages.success(request, "Vous êtes maintenant connecté.")
            return redirect('home')

        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    else:
        form = UserLoginForm()
        messages.info(request, "Connectez-vous à votre compte en remplissant le formulaire ci-dessous.")

    return render(request, 'Users/auths/login.html', {'form': form})

def activate(request, uidb64, token):

    if request.user.is_active:
        messages.info(request, "Votre compte est déjà activé. Veuillez vous connecter.")
        return redirect('login')
    
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Fab_User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Fab_User.DoesNotExist):
        user = None

    # si l'utilisateur existe et que le token est valide
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitations ! Votre compte a été activé avec succès.')
        return redirect('login')
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

            # Send verification email
            mail_subject = 'Veuillez activer votre compte.'
            email_template = 'Users/emails/account_verification.html'
            protocol = 'https' if request.is_secure() else 'http'
            domain = get_current_site(request).domain

            #send_verification_email.delay(protocol, domain, user.pk, mail_subject, email_template)
            #send_verification_email(protocol, domain, user.pk, mail_subject, email_template)


            messages.success(request, "Votre compte a été créé avec succès! Veuillez vérifier votre e-mail pour activer votre compte.")
            #return redirect('login')
            #login(request, user)
            return redirect('login')
        else:
            return render(request, "Users/auths/signup.html", {'form': form})
    else:
        return render(request, 'Users/auths/signup.html', context={'form': UserSignUpForm()})

@login_required
def user_home(request):
    print("you're in view user_home")
    #check_user_activated(request.user, request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    # si l'utilisateur est un superuser, rediriger vers la page d'administration
    if user.is_superuser or user.is_staff:
        print("redirecting to admin")
        return redirect('/admin')
    print("rendering user home")
    return render(request ,'Users/home/index.html', {'user':user})

@login_required
def user_edit(request):
    #check_user_activated(request.user, request)
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
    #check_user_activated(request.user, request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/orders/index.html", {'user':user})

@login_required
def user_favourites(request):
    #check_user_activated(request.user, request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/favourites/index.html", {'user':user})

@login_required
def user_tracked_deliveries(request):
    #check_user_activated(request.user, request)
    user = get_object_or_404(Fab_User,uuid=request.user.uuid)
    return render(request, "Users/tracked_deliveries/index.html", {'user':user})
