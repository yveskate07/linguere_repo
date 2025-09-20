import os
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from Formations.forms import SignedUpUserForm, BrochureForm, RequestForm
from Formations.models import Formations
from mail_sender import brochure_to_client_through_mail, mail_to_fablab, mail_to_the_client


#SCRIPT_PATH = Path(__file__).resolve()
#JSON_PATH = SCRIPT_PATH.parent / 'static' / 'Formations' / 'data' / 'data.json'

# Create your views here.

@login_required
def formationView(request, formation_name):

    formation = Formations.objects.get(slug=formation_name)

    duration = int(formation.duration.total_seconds() // 3600)

    modules = [mod.name for mod in formation.Modules.all()]
    prerequisites = [(p.image.url,p.name, p.level) for p in formation.Prerequisites.all()]
    skillgained = [(s.name, s.description_skill) for s in formation.SkillsGained.all()]
    m_points = [(mp.name,mp.description) for mp in formation.MotivPoints.all()]
    advantages = [(a.name, a.description) for a in formation.Advantages.all()]

    form1 = SignedUpUserForm()
    form2 = BrochureForm()
    form3 = RequestForm()

    return render(request, 'Formations/index.html',
                      {'formSignedUpUser': form1, 'formBrochure': form2, 'formRequest': form3,
                       'formation_image_url':formation.image.url,
                       'formation': formation,
                       'duration':duration,
                       'modules_':modules if len(modules)>0 else None,
                       'prerequisites_':prerequisites if len(prerequisites)>0 else None,
                       'skillgained_':skillgained if len(skillgained)>0 else None,
                       'm_points':m_points if len(m_points)>0 else None,
                       'advantages_':advantages if len(advantages)>0 else None})


def SigningUp(request, formation_name):
    if request.method == "POST":
        form = SignedUpUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_inscription'))
            user.save()

            # envoi d'un mail au client puis notification a linguere
            mail_to_the_client(formation_name=formation_name, user={'name':user.name, 'e-mail':user.email, 'formation':user.formation.name, 'message':request.POST.get('message')})

        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return formationView(request, formation_name)


def returnBrochure(request, formation_name):
    if request.method == "POST":
        form = BrochureForm({'name':request.POST.get('name'), 'email':request.POST.get('email'),
                             'tel_number':request.POST.get('tel_number'), 'availability':request.POST.get('availability'),
                             'message':request.POST.get('message')})
        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_brochure'))
            user.save()

            # envoi de la brochure par mail puis notification a linguere
            brochure_to_client_through_mail(receiver_email=user.email, formation_name=formation_name, msg_=request.POST.get('message'), user={'name':user.name, 'e-mail':user.email, 'formation':user.formation.name, "message":request.POST.get('message')})

        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite !!!"})

    return formationView(request, formation_name)


def userGetInTouch(request, formation_name):
    if request.method == "POST":
        form = RequestForm({'name': request.POST.get('name'), 'email': request.POST.get('email'),
                            'tel_number': request.POST.get('tel_number'), 'message': request.POST.get('message')})

        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_contact'))
            user.save()

            # envoi d'alerte a linguere
            mail_to_fablab(formation_name=formation_name, user={'name':user.name, 'e-mail':user.email, 'formation':user.formation.name, "message": request.POST.get('message')}, msg_=request.POST.get('message'))


        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return formationView(request, formation_name)