import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from Activities.models import Activity
from Formations.models import Formations
from Services.models import Service
from Users.auth_form import UserLoginForm, UserSignUpForm


def test_celery(request):
    from Formations.tasks import double_nombre
    task = double_nombre.delay(10)
    return JsonResponse({'task_id': task.id})

def status_celery(request, task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    return JsonResponse({
        "state": result.state,
        "result": result.result
    })

class FabLabLogoutView(LogoutView):
    next_page = '/login'

    
def FabLabLoginView(request):
    messages.info(request, "Connectez-vous à votre compte en remplissant le formulaire ci-dessous.")
    return render(request, 'Users/auths/login.html', context={'form': UserLoginForm()})

def signUpView(request):
    '''if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin:index')
        return redirect('home')
    return render(request, 'Users/registration/signup.html', context={'form': UserSignUpForm()})'''

    if request.user.is_authenticated:
        return redirect('home')
    
    messages.info(request, "Créez votre compte en remplissant le formulaire ci-dessous.")
    return render(request, 'Users/auths/signup.html', context={'form': UserSignUpForm()})


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

    context['formation_available'] = context['formation_laser'] and context['formation_laser'] and context['formation_laser'] and context['formation_laser'] and context['formation_laser']

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