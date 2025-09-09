import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from Formations.models import Formations
from Shop.services.cart_service import CartService
from Users.auth_form import UserLoginForm, UserSignUpForm
from Users.models import Fab_User


class FabLabLogoutView(LogoutView):
    next_page = '/login'


class FabLabLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    model = Fab_User
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Redirige vers la page de login après inscription

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # print("********************* le formulaire est invalide *********************")
        # from pprint import pprint
        # pprint(form.errors.as_data())
        return self.render_to_response(self.get_context_data(form=form))

def redirect_404(request, exception):
    return redirect('home')

@login_required
def home(request):

    broderie_num = Formations.objects.get(name="Broderie Numérique")
    fraiseuse_num = Formations.objects.get(name="Fraiseuse Numérique (CNC)")
    impression_3d = Formations.objects.get(name="Impression 3D")
    impression_num = Formations.objects.get(name="Impression Numérique")
    laser = Formations.objects.get(name="Découpe Laser")
    products_cart = CartService.get_cart_data_from_request(request)
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'

    return render(request,'AntaBackEnd/accueil/index.html',
                  {'broderie_num_slug': broderie_num.slug,
                        'fraiseuse_num_slug': fraiseuse_num.slug,
                        'impression_3d_slug': impression_3d.slug,
                        'impression_num_slug': impression_num.slug,
                        'laser_slug': laser.slug,
                        'user_id': user_id,
                        'products_cart': products_cart['products'],
                        'products_cart_js': json.dumps(products_cart['products']),
                        'total_price_cart': products_cart['total_price']
                                   }
                  )

@login_required
def location(request):
    products_cart = CartService.get_cart_data_from_request(request)
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request, 'AntaBackEnd/location/index.html', context={
        'products_cart': products_cart['products'],
        'user_id': user_id,
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})

@login_required
def about(request):
    products_cart = CartService.get_cart_data_from_request(request)
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request, "AntaBackEnd/about/index.html", context={
        'products_cart': products_cart['products'],
        'user_id': user_id,
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price']})

class FabPassResetView(PasswordResetView):
    subject_template_name = "registration/password_reset_subject.txt"

class FabPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')