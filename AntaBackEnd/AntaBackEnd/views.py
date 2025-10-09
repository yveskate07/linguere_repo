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

@login_required
def home(request):

    broderie_num = Formations.objects.get(name="Broderie Numérique")
    fraiseuse_num = Formations.objects.get(name="Fraiseuse Numérique (CNC)")
    impression_3d = Formations.objects.get(name="Impression 3D")
    impression_num = Formations.objects.get(name="Impression Numérique")
    laser = Formations.objects.get(name="Découpe Laser")
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    serv_imp_num_prop = Service.objects.filter(name__in = ['Impression sur Papier et Supports Rigides',
                                                    'Impression sur Textiles et Vêtements',
                                                    'Impression sur Objets Personnalisés'])
    other_services = Service.objects.filter(name__in = ['Broderie Numérique',
                                                        'Service de Fraiseuse Numérique (CNC)',
                                                        'Découpe et Gravure Laser',
                                                        "Service d'Impression 3D"])
    activities = Activity.objects.all()

    return render(request,'AntaBackEnd/accueil/index.html',
                  {'formation_broderie_num': broderie_num,
                        'formation_fraiseuse_num': fraiseuse_num,
                        'formation_impression_3d': impression_3d,
                        'formation_impression_num': impression_num,
                        'formation_laser': laser,
                        'other_services':other_services,
                        'serv_imp_num_prop': serv_imp_num_prop,
                        'user_id': user_id,
                        'activities': activities,
                                   }
                  )

@login_required
def location(request):
    user_id = request.user.uuid if request.user.is_authenticated else 'anonymous_id'
    return render(request, 'AntaBackEnd/location/index.html', context={
        'user_id': user_id,})

@login_required
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