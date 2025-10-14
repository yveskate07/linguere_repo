import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from Activities.models import Activity
from Formations.models import Formations
from Services.models import Service
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
        return self.render_to_response(self.get_context_data(form=form))

def redirect_404(request, exception):
    return redirect('home')


def home(request):

    context = dict()

    try:
        broderie_num = Formations.objects.get(name="Broderie Numérique")
        context['formation_broderie_num'] = broderie_num
    except Exception:
        context['formation_broderie_num'] = None

    try:
        fraiseuse_num = Formations.objects.get(name="Fraiseuse Numérique (CNC)")
        context['formation_fraiseuse_num'] = fraiseuse_num
    except Exception:
        context['formation_fraiseuse_num'] = None

    try:
        impression_3d = Formations.objects.get(name="Impression 3D")
        context['formation_impression_3d'] = impression_3d
    except Exception:
        context['formation_impression_3d'] = None

    try:
        impression_num = Formations.objects.get(name="Impression Numérique")
        context['formation_impression_num'] = impression_num
    except Exception:
        context['formation_impression_num'] = None

    try:
        laser = Formations.objects.get(name="Découpe Laser")
        context['formation_laser'] = laser
    except Exception:
        context['formation_laser'] = None

    context['user_id'] = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    context['serv_imp_num_prop'] = Service.objects.filter(name__in = ['Impression sur Papier et Supports Rigides',
                                                    'Impression sur Textiles et Vêtements',
                                                    'Impression sur Objets Personnalisés'])

    context['other_services'] = Service.objects.filter(name__in = ['Broderie Numérique',
                                                        'Service de Fraiseuse Numérique (CNC)',
                                                        'Découpe et Gravure Laser',
                                                        "Service d'Impression 3D"])
    context['activities'] = Activity.objects.all()

    return render(request,'AntaBackEnd/accueil/index.html',context=context)


def location(request):
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request, 'AntaBackEnd/location/index.html', context={
        'user_id': user_id,})


def about(request):
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request, "AntaBackEnd/about/index.html", context={
        'user_id': user_id,})

class FabPassResetView(PasswordResetView):
    subject_template_name = "registration/password_reset_subject.txt"

class FabPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')