from django.http import HttpResponseRedirect
from django.shortcuts import render

from Formations.forms import SignedUpUserForm, BrochureForm, RequestForm
from Formations.models import Formations, Module, Prerequisites, SkillGained, MotivPoints, Advantages


# Create your views here.
def formationView(request, formation_name):

    formation = Formations.objects.get(slug=formation_name)
    modules = Module.objects.filter(formation=formation.pk)
    prerequisites = Prerequisites.objects.filter(formation=formation.pk)
    gainedskills = SkillGained.objects.filter(formation=formation.pk)
    motiv_points = MotivPoints.objects.filter(formation=formation.pk)
    advantages = Advantages.objects.filter(formation=formation.pk)


    f_name = formation.name
    motiv = formation.motiv
    price = formation.price
    duration = int(formation.duration.total_seconds() // 3600)
    nb_h_per_week = formation.hours_per_week
    availability = formation.availability

    det_plus_name = formation.determinant +' '+ formation.name
    modules_ = [mod.name for mod in modules]
    prerequisites_ = [(p.image.url,p.name, p.level) for p in prerequisites]
    skillgained_ = [(s.name, s.description_skill) for s in gainedskills]
    m_points = [(mp.name,mp.description) for mp in motiv_points]
    advantages_ = [(a.name, a.description) for a in advantages]

    form1 = SignedUpUserForm()
    form2 = BrochureForm()
    form3 = RequestForm()

    return render(request, 'Formations/index.html',
                      {'formSignedUpUser': form1, 'formBrochure': form2, 'formRequest': form3,
                       'formation_image_url':formation.image.url,
                       'id_formation': formation.id,'slug':formation.slug,
                       'f_name':f_name,
                       'motiv':motiv,
                       'price':price,
                       'duration':duration,
                       'nb_h_per_week':nb_h_per_week,
                       'availability':availability,
                       'det_plus_name':det_plus_name,
                       'modules_':modules_,
                       'prerequisites_':prerequisites_,
                       'skillgained_':skillgained_,
                       'm_points':m_points,
                       'advantages_':advantages_})


def SigningUp(request, formation_name):
    if request.method == "POST":
        form = SignedUpUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_inscription'))
            user.save()

            return render(request, 'Formations/success/index.html', {'msg': f'Vous êtes inscrit à la formation {user.formation.name} !!!'})
        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return HttpResponseRedirect(request.path)


def returnBrochure(request, formation_name):
    if request.method == "POST":
        form = BrochureForm({'name':request.POST.get('name'), 'email':request.POST.get('email'),
                             'tel_number':request.POST.get('tel_number'), 'availability':request.POST.get('availability'),
                             'message':request.POST.get('message')})
        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_brochure'))
            user.save()

            # envoi de la brochure par mail
            #
            return render(request, 'Formations/success/index.html', {'msg':'Vous avez reçu la brochure par mail !!!'})
        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite !!!"})

    return HttpResponseRedirect(request.path)

def userGetInTouch(request, formation_name):
    if request.method == "POST":
        form = RequestForm({'name': request.POST.get('name'), 'email': request.POST.get('email'),
                            'tel_number': request.POST.get('tel_number'), 'message': request.POST.get('message')})

        if form.is_valid():
            user = form.save(commit=False)
            user.formation = Formations.objects.get(id=request.POST.get('id_formation_contact'))
            user.save()

            # envoie du message par mail
            #
            return render(request, 'Formations/success/index.html', {'msg': 'Nous vous contacterons !!!'})
        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return HttpResponseRedirect(request.path)
