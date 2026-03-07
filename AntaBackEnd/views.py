import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from Activities.models import Activity
from Formations.models import Formations
from Services.models import ServiceInfo
from Users.auth_form import UserLoginForm, UserSignUpForm
from Partners.models import Partner
from New_features.models import Feature

"""def test_celery(request):
    from Formations.tasks import double_nombre
    task = double_nombre.delay(10)
    return JsonResponse({'task_id': task.id})"""

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

    right_first_row = Formations.objects.filter(css_cls_parent_in_home="droite")

    left_first_row = Formations.objects.filter(css_cls_parent_in_home="gauche")

    second_row = Formations.objects.filter(css_cls_parent_in_home="pleine-largeur")

    context['right_first_row'] = right_first_row
    context['left_first_row'] = left_first_row
    context['second_row'] = second_row

    context['formation_available'] = right_first_row.exists() or left_first_row.exists() or second_row.exists()

    context['serv_imp_num_prop'] = ServiceInfo.objects.filter(impressionNumerique = True)

    context['other_services'] = ServiceInfo.objects.filter(impressionNumerique = False)
    context['activities'] = Activity.objects.all()

    context['partners'] = Partner.objects.all()

    context['features'] = Feature.objects.all()

    return render(request,'AntaBackEnd/accueil/index.html',context=context)


def location(request):
    return render(request, 'AntaBackEnd/location/index.html')


def about(request):
    return render(request, "AntaBackEnd/about/index.html")