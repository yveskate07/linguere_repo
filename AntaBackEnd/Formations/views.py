from django.http import HttpResponseRedirect
from django.shortcuts import render

from Formations.forms import SignedUpUserForm, BrochureForm, RequestForm
from Formations.models import Formations


# Create your views here.
def formationView(request, formation_name):

    broderie_num = Formations.objects.get(name="Broderie Numérique")
    fraiseuse_num = Formations.objects.get(name="Fraiseuse Numérique (CNC)")
    impression_3d = Formations.objects.get(name="Impression 3D")
    impression_num = Formations.objects.get(name="Impression Numérique")
    laser = Formations.objects.get(name="Découpe Laser")

    FORMATIONS = {broderie_num.slug: 'Formations/broderie_num/index.html',
                  fraiseuse_num.slug: 'Formations/fraiseuse_num/index.html',
                  impression_3d.slug: 'Formations/impression_3d/index.html',
                  impression_num.slug: 'Formations/impression_num/index.html',
                  laser.slug: 'Formations/laser/index.html'}

    template_name = FORMATIONS[formation_name]

    formation = {broderie_num.slug: broderie_num,
                  fraiseuse_num.slug: fraiseuse_num,
                  impression_3d.slug: impression_3d,
                  impression_num.slug: impression_num,
                  laser.slug: laser}[formation_name]

    form1 = SignedUpUserForm()
    form2 = BrochureForm()
    form3 = RequestForm()

    return render(request, template_name,
                      {'formSignedUpUser': form1, 'formBrochure': form2, 'formRequest': form3,
                       'id_formation': formation.id,'slug':formation.slug})


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
        form = BrochureForm({'name':request.POST.get('name'), 'email':request.POST.get('email'), 'tel_number':request.POST.get('tel_number'), 'method':request.POST.get('method')})
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
        form = RequestForm({'name': request.POST.get('contact-name'), 'email': request.POST.get('contact-email'),
                            'tel_number': request.POST.get('contact-tel_number'), 'method': request.POST.get('contact-method')})

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
