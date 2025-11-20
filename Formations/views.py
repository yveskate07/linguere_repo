from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import SignedUpUserForm, BrochureForm, RequestForm
from .models import Formations
from .tasks import brochure_to_client_through_mail, mail_to_fablab, mail_to_the_client



# Create your views here.

@login_required
def formationView(request, formation_name):
    try:
        formation = Formations.objects.get(slug=formation_name)
    except Formations.DoesNotExist:
        return render(request, 'Formations/error/index.html', {'msg': "La formation que vous recherchez n'existe pas!!!"})
    else:
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

@login_required
def SigningUp(request, formation_name):
    if request.method == "POST":
        form = SignedUpUserForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            try:
                data.formation = Formations.objects.get(id=request.POST.get('id_formation_inscription'))
                data.user = request.user
                data.save()
            except Formations.DoesNotExist:
                return render(request, 'Formations/error/index.html', {'msg': "La formation que vous recherchez n'existe pas!!!"})
            else:
                # envoi d'un mail au client puis notification a linguere
                mail_to_the_client.delay(formation_name=formation_name, 
                                   user={'name':data.name, 
                                         'e-mail':data.email, 
                                         'message':request.POST.get('message')})
                
                mail_to_fablab.delay(formation_name=formation_name, 
                               reason='new inscription', 
                               admin_edit_view = f"/admin/Formations/signedupuser/{data.pk}/change/",
                               user={'name':data.name, 
                                     'e-mail':data.email, 
                                     'message':request.POST.get('message')})

        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return formationView(request, formation_name)

@login_required
def returnBrochure(request, formation_name):
    if request.method == "POST":
        form = BrochureForm({'availability':request.POST.get('availability'), 'message':request.POST.get('message')})
        if form.is_valid():
            data = form.save(commit=False)
            try:
                data.formation = Formations.objects.get(id=request.POST.get('id_formation_brochure'))
                data.user = request.user
                data.save()
            except Formations.DoesNotExist:
                return render(request, 'Formations/error/index.html', {'msg': "La formation que vous recherchez n'existe pas!!!"})

            else:
                # envoi de la brochure par mail puis notification a linguere
                brochure_to_client_through_mail.delay(receiver_email=data.user.email, formation_name=data.formation.name, 
                                                admin_edit_view = f"/admin/Formations/userbrochure/{data.pk}/change/",
                                                user={'name':data.user.name, 
                                                'e-mail':data.user.email, 
                                                "message":request.POST.get('message')
                                            })

        else:
            return render(request, 'Formations/error/index.html', {'msg': "Remplissez correctement le formulaire !"})

    return formationView(request, formation_name)

@login_required
def userGetInTouch(request, formation_name):
    if request.method == "POST":
        form = RequestForm({'message': request.POST.get('message')})

        if form.is_valid():
            data = form.save(commit=False)
            try:
                data.formation = Formations.objects.get(id=request.POST.get('id_formation_contact'))
                data.user = request.user
                data.save()
            except Formations.DoesNotExist:
                return render(request, 'Formations/error/index.html', {'msg': "La formation que vous recherchez n'existe pas!!!"})
            else:
                # envoi d'alerte a linguere
                mail_to_fablab.delay(formation_name=formation_name, 
                               reason='information request',
                               admin_edit_view = f"/admin/Formations/userrequest/{data.pk}/change/",
                               user={'name':data.user.name, 
                                     'e-mail':data.user.email})


        else:
            return render(request, 'Formations/error/index.html', {'msg': "Une erreur s'est produite!!!"})

    return formationView(request, formation_name)