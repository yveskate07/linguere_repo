import json

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Services.forms import Broderie_num_customForm1, Fraiseuse_customForm1, Laser_customForm1, Imp_3D_customForm1, \
    Broderie_num_customForm2, Fraiseuse_customForm2, Laser_customForm2, Imp_3D_customForm2, Paper_customForm1, \
    Paper_customForm2, Textile_customForm1, Textile_customForm2, Objects_customForm1, Objects_customForm2
from Services.models import Service
from mail_sender import mail_to_the_client, mail_to_fablab


def get_msg_for_client_mail(Service_name, obj, width, height, quantite, comment, msg_deliver, img_path=None, colors=None):

    colors_html = ""
    colors_css = ""
    if colors:
        colors_html = "<p><span class='highlight'>Couleurs souhaitées </span>: "+' '.join([f"""<div class="circle-{i.lstrip('#')}"></div>""" for i in colors]) + "</p>"
        colors_css = ' '.join([f"""
        .circle-{color.lstrip('#')}""" + """ {
            width: 15px; 
            height: 15px;
            background-color:"""+f""" {color}"""+""";
            border-radius: 50%;  
            margin-bottom: 12px;
        }""" for color in colors])

    msg_body = """
        <!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmation de réception de votre commande</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #eeeeee;
            margin-bottom: 20px;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eeeeee;
            font-size: 0.9em;
            color: #777777;
        }
        .order-details {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .order-details p {
            margin: 5px 0;
        }
        .highlight {
            font-weight: bold;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 15px;
        }"""+colors_css+ f"""
    </style>
</head>
<body>
    <div class="header">
        <h2>Confirmation de réception de votre commande</h2>
    </div>

    <p>Bonjour,</p>

    <p>Nous vous remercions pour votre commande <span class="highlight">{Service_name}</span> : {obj}.</p>

    <div class="order-details">
        <p>Nous vous confirmons que nous avons bien reçu votre demande de personnalisation avec les indications suivantes :</p>

        <p><span class="highlight">Objet :</span> {obj}</p>
        <p><span class="highlight">Dimensions du design </span>: {width} (largeur) x {height} (longueur)</p>
        <p><span class="highlight">Quantité </span>: {quantite} exemplaires</p>
        {colors_html}
        <p><span class="highlight">Commentaire </span>: {comment}</p>
        <p><span class="highlight">Image du design choisi: </span>: <img src={img_path} alt="design picture"/></p>
    </div>

    <p>Votre commande est actuellement en cours de traitement.<br>{msg_deliver}

    <p>N'hésitez pas à nous contacter si vous avez des questions ou des précisions à apporter.</p>

    <div class="footer">
        <p>Cordialement,</p>
        <p><strong>Linguere FabLab</strong><br>
        Service Client</p>
        <p>linguerefablab@gmail.com | +221 77 314 66 62</p>
    </div>

</body>
</html>
"""

    return msg_body


def get_msg_for_admin_mail(request , **kwargs):
    admin_url = reverse('admin:index')
    absolute_admin_url = request.build_absolute_uri(admin_url)
    colors_html = ""
    colors_css = ""
    colors = kwargs.get('colors', None)

    if colors:

        colors_html = "<p><span class='highlight'>Couleurs souhaitées </span>: " + ' '.join([f"""<div class="circle-{i.lstrip('#')}"></div>""" for i in colors]) + "</p>"
        colors_css = ' '.join([f"""
                .circle-{color.lstrip('#')}""" + """ {
                    width: 15px; 
                    height: 15px;
                    background-color: """+f"""{color}"""+""";
                    border-radius: 50%;  /* Rend l'élément circulaire */
                    margin-bottom: 12px;
                }""" for color in colors])

    msg_body = """
    <!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nouvelle commande enregistrée</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 650px;
            margin: 0 auto;
            padding: 25px;
            background-color: #f5f5f5;
        }
        .email-container {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #eaeaea;
            margin-bottom: 25px;
        }
        .header h2 {
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .order-details {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .detail-item {
            margin-bottom: 12px;
            display: flex;
        }
        .detail-label {
            font-weight: 600;
            color: #2c3e50;
            min-width: 180px;
        }
        .divider {
            height: 1px;
            background-color: #eaeaea;
            margin: 25px 0;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eaeaea;
            font-size: 0.9em;
            color: #7f8c8d;
            text-align: center;
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
            font-weight: 500;
        }
        .highlight {
            color: #e74c3c;
            font-weight: 600;
        }"""+colors_css+ f"""
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h2>Nouvelle commande enregistrée</h2>
            <p style="color: #7f8c8d;">Linguere FabLab</p>
        </div>

        <p>Bonjour Linguere FabLab, une nouvelle commande a été passée sur le site.</p>

        <div class="order-details">
            <h3 style="margin-top: 0; color: #3498db;">Détails de la commande :</h3>

            <div class="detail-item">
                <span class="detail-label">Service :</span>
                <span>{kwargs['service']}</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">Objet :</span>
                <span>{kwargs['obj']}</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">Dimensions du design :</span>
                <span>{kwargs['width']} (largeur) x {kwargs['height']} (longueur)</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">Quantité :</span>
                <span>{kwargs['quantity']} exemplaires</span>
            </div>

            {colors_html}

            <div class="detail-item">
                <span class="detail-label">Commentaire :</span>
                <span>{kwargs['comment']}</span>
            </div>
            
            <div class="detail-item">
                <span class="detail-label">Image du design choisi: </span>
                <img src={kwargs['img_path']} alt="design picture"/>
            </div>

            <div class="detail-item">
                <span class="detail-label">Mode de livraison :</span>
                <span>{kwargs['delivery']}</span>
            </div>

            <div class="divider"></div>

            <div class="detail-item">
                <span class="detail-label">Nom du client :</span>
                <span>{kwargs.get('name')}</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">E-mail du client :</span>
                <span>{kwargs.get('email')}</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">Téléphone :</span>
                <span>{kwargs.get('tel_number')}</span>
            </div>

            <div class="detail-item">
                <span class="detail-label">Ville :</span>
                <span>{kwargs.get('town')}</span>
            </div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <a href="{absolute_admin_url}" class="button">Voir la commande</a>
        </div>

        <div class="footer">
            <p>Ceci est une notification automatique - merci de ne pas répondre à cet email</p>
            <p>© 2023 Linguere FabLab. Tous droits réservés.</p>
        </div>
    </div>
</body>
</html>
"""

    return msg_body


# Create your views here.
def broderie_numerique(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Broderie Numérique")
    return render(request, "Services/broderie/index.html", {'broderie_form1': Broderie_num_customForm1(),
                                                            'broderie_form2': Broderie_num_customForm2(),
                                                            'service_id': service.pk,
                                                            'brod_serviceName': service.name,
                                                            'brod_serviceDesc': service.description,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url,
                                                            'errors': errors,'errors_txt':errors_txt})


def fraiseuse_numerique(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Service de Fraiseuse Numérique (CNC)")
    return render(request, "Services/fraiseuse/index.html", {'fraiseuse_form1': Fraiseuse_customForm1(),
                                                             'fraiseuse_form2': Fraiseuse_customForm2(),
                                                             'service_id': service.pk,
                                                             'frais_serviceName': service.name,
                                                             'frais_serviceDesc': service.description,
                                                             'img1': service.image1.url, 'img2': service.image2.url,
                                                             'img3': service.image3.url, 'img4': service.image4.url,
                                                             'img5': service.image5.url, 'img6': service.image6.url,
                                                             'img7': service.image7.url, 'img8': service.image8.url,
                                                             'errors': errors,'errors_txt':errors_txt})


def decoupe_laser(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Découpe et Gravure Laser")
    return render(request, "Services/laser/index.html", {'laser_form1': Laser_customForm1(),
                                                         'laser_form2': Laser_customForm2(),
                                                         'service_id': service.pk,
                                                         'laser_serviceName': service.name,
                                                         'laser_serviceDesc': service.description,
                                                         'img1': service.image1.url, 'img2': service.image2.url,
                                                         'img3': service.image3.url, 'img4': service.image4.url,
                                                         'img5': service.image5.url, 'img6': service.image6.url,
                                                         'img7': service.image7.url, 'img8': service.image8.url,
                                                         'errors': errors,'errors_txt':errors_txt})


def impression_3D(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Service d'Impression 3D")
    return render(request, 'Services/Impre_3D/index.html', {'imp_3D_form1': Imp_3D_customForm1(),
                                                            'imp_3D_form2': Imp_3D_customForm2(),
                                                            'service_id': service.pk,
                                                            'imp_3D_serviceName': service.name,
                                                            'imp_3D_serviceDesc': service.description,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url,
                                                            'errors': errors,'errors_txt':errors_txt})


def impression_num_papiers(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Papier et Supports Rigides")
    return render(request, 'Services/Impre_Num_Prop/paper_solid_support/index.html',
                  {'paper_form1': Paper_customForm1(),
                   'paper_form2': Paper_customForm2(),
                   'paper_serviceName': service.name,
                   'paper_serviceDesc': service.description,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
                   'img8': service.image8.url, 'errors': errors,'errors_txt':errors_txt})


def impression_num_textile(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Textiles et Vêtements")
    return render(request, 'Services/Impre_Num_Prop/textile_vetements/index.html',
                  {'textile_form1': Textile_customForm1(),
                   'textile_form2': Textile_customForm2(),
                   'textile_serviceName': service.name,
                   'textile_serviceDesc': service.description,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
                   'img8': service.image8.url, 'errors': errors,'errors_txt':errors_txt})


def impression_num_objects(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Objets Personnalisés")
    return render(request, 'Services/Impre_Num_Prop/others_objects/index.html', {'object_form1': Objects_customForm1(),
                                                                                 'object_form2': Objects_customForm2(),
                                                                                 'object_serviceName': service.name,
                                                                                 'object_serviceDesc': service.description,
                                                                                 'service_id': service.pk,
                                                                                 'img1': service.image1.url,
                                                                                 'img2': service.image2.url,
                                                                                 'img3': service.image3.url,
                                                                                 'img4': service.image4.url,
                                                                                 'img5': service.image5.url,
                                                                                 'img6': service.image6.url,
                                                                                 'img7': service.image7.url,
                                                                                 'img8': service.image8.url,
                                                                                 'errors': errors,'errors_txt':errors_txt})


def save_broderie_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Broderie_num_customForm1({'support_type': request.POST.get('support_type'),
                                             'other_support': request.POST.get('other_support'),
                                             'dim_1': request.POST.get('dim_1'),
                                             'dim_2': request.POST.get('dim_2'),
                                             'quantity': request.POST.get('quantity'),
                                             'special_instructions': request.POST.get('special_instructions'),
                                             'design_picture': request.POST.get('design_picture'),
                                             'codeCouleur': request.POST.get('codeCouleur'),
                                             'name': request.POST.get('name'),
                                             'email': request.POST.get('email'),
                                             'tel_number': request.POST.get('tel_number'),
                                             'town': request.POST.get('town'),
                                             'delivery_mode': request.POST.get('delivery_mode'),
                                             'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Broderie_num_customForm2({'support_type': request.POST.get('support_type'),
                                                    'other_support': request.POST.get('other_support'),
                                                    'dim_1': request.POST.get('dim_1'),
                                                    'dim_2': request.POST.get('dim_2'),
                                                    'quantity': request.POST.get('quantity'),
                                                    'special_instructions': request.POST.get('special_instructions'),
                                                    'upload_design_picture': request.POST.get('upload_design_picture'),
                                                    'codeCouleur': request.POST.get('codeCouleur'),
                                                    'name': request.POST.get('name'),
                                                    'email': request.POST.get('email'),
                                                    'tel_number': request.POST.get('tel_number'),
                                                    'town': request.POST.get('town'),
                                                    'delivery_mode': request.POST.get('delivery_mode'),
                                                    'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)
            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""


            msg_body1 = get_msg_for_client_mail(Service_name='Broderie',
                                                obj=request.POST.get('support_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                colors=request.POST.get('codeCouleur').split(','),
                                                comment = request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Broderie Numérique", obj=request.POST.get('support_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Broderie Numérique")

            return broderie_numerique(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return broderie_numerique(request, errors=1, errors_txt=errors)


def save_fraiseuse_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Fraiseuse_customForm1({'service_type': request.POST.get('service_type'),
                                          'dim_1': request.POST.get('dim_1'),
                                          'dim_2': request.POST.get('dim_2'),
                                          'quantity': request.POST.get('quantity'),
                                          'special_instructions': request.POST.get('special_instructions'),
                                          'design_picture': request.POST.get('design_picture'),
                                          'used_materials': request.POST.get('used_materials'),
                                          'name': request.POST.get('name'),
                                          'email': request.POST.get('email'),
                                          'tel_number': request.POST.get('tel_number'),
                                          'town': request.POST.get('town'),
                                          'delivery_mode': request.POST.get('delivery_mode'),
                                          'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Fraiseuse_customForm2({'service_type': request.POST.get('service_type'),
                                                 'dim_1': request.POST.get('dim_1'),
                                                 'dim_2': request.POST.get('dim_2'),
                                                 'quantity': request.POST.get('quantity'),
                                                 'special_instructions': request.POST.get('special_instructions'),
                                                 'upload_design_picture': request.POST.get('upload_design_picture'),
                                                 'used_materials': request.POST.get('used_materials'),
                                                 'name': request.POST.get('name'),
                                                 'email': request.POST.get('email'),
                                                 'tel_number': request.POST.get('tel_number'),
                                                 'town': request.POST.get('town'),
                                                 'delivery_mode': request.POST.get('delivery_mode'),
                                                 'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name='Fraiseuse',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                img_path=design_path,
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Fraiseuse Numérique", obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=None,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body1,
                               subject="Confirmation de réception de votre commande")
            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Fraiseuse Numérique", )
            return fraiseuse_numerique(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return fraiseuse_numerique(request, errors=1, errors_txt=errors)


def save_laser_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Laser_customForm1({'service_type': request.POST.get('service_type'),
                                      'dim_1': request.POST.get('dim_1'),
                                      'dim_2': request.POST.get('dim_2'),
                                      'quantity': request.POST.get('quantity'),
                                      'special_instructions': request.POST.get('special_instructions'),
                                      'design_picture': request.POST.get('design_picture'),
                                      'used_materials': request.POST.get('used_materials'),
                                      'name': request.POST.get('name'),
                                      'email': request.POST.get('email'),
                                      'tel_number': request.POST.get('tel_number'),
                                      'town': request.POST.get('town'),
                                      'delivery_mode': request.POST.get('delivery_mode'),
                                      'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Laser_customForm2({'service_type': request.POST.get('service_type'),
                                             'dim_1': request.POST.get('dim_1'),
                                             'dim_2': request.POST.get('dim_2'),
                                             'quantity': request.POST.get('quantity'),
                                             'special_instructions': request.POST.get('special_instructions'),
                                             'upload_design_picture': request.POST.get('upload_design_picture'),
                                             'used_materials': request.POST.get('used_materials'),
                                             'name': request.POST.get('name'),
                                             'email': request.POST.get('email'),
                                             'tel_number': request.POST.get('tel_number'),
                                             'town': request.POST.get('town'),
                                             'delivery_mode': request.POST.get('delivery_mode'),
                                             'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name="Découpe Laser",
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                img_path=design_path,
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Découpe Laser", obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=None,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")
            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Découpe Laser", )
            return decoupe_laser(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return decoupe_laser(request, errors=1, errors_txt=errors)


def save_imp_3d_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Imp_3D_customForm1({'impression_type': request.POST.get('impression_type'),
                                       'dim_1': request.POST.get('dim_1'),
                                       'dim_2': request.POST.get('dim_2'),
                                       'quantity': request.POST.get('quantity'),
                                       'codeCouleur': request.POST.get('codeCouleur'),
                                       'special_instructions': request.POST.get('special_instructions'),
                                       'design_picture': request.POST.get('design_picture'),
                                       'used_materials': request.POST.get('used_materials'),
                                       'name': request.POST.get('name'),
                                       'email': request.POST.get('email'),
                                       'tel_number': request.POST.get('tel_number'),
                                       'town': request.POST.get('town'),
                                       'delivery_mode': request.POST.get('delivery_mode'),
                                       'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = Imp_3D_customForm2({'impression_type': request.POST.get('impression_type'),
                                       'dim_1': request.POST.get('dim_1'),
                                       'dim_2': request.POST.get('dim_2'),
                                       'quantity': request.POST.get('quantity'),
                                       'codeCouleur': request.POST.get('codeCouleur'),
                                       'special_instructions': request.POST.get('special_instructions'),
                                       'upload_design_picture': request.POST.get('upload_design_picture'),
                                       'used_materials': request.POST.get('used_materials'),
                                       'name': request.POST.get('name'),
                                       'email': request.POST.get('email'),
                                       'tel_number': request.POST.get('tel_number'),
                                       'town': request.POST.get('town'),
                                       'delivery_mode': request.POST.get('delivery_mode'),
                                       'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name='Impression 3D',
                                                obj=request.POST.get('impression_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                colors=request.POST.get('codeCouleur').split(','),
                                                img_path=design_path,
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Impression 3D", obj=request.POST.get('impression_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression 3D", )

            return impression_3D(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_3D(request, errors=1, errors_txt=errors)


def save_imp_text_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Textile_customForm1.Meta.fields}
            form = Textile_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Textile_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Textile_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name='Impression Textile',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Textile',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               img_path=design_path,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))
            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Textile", )

            return impression_num_textile(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_textile(request, errors=1, errors_txt=errors)


def save_imp_paper_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Paper_customForm1.Meta.fields}
            form = Paper_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Paper_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Paper_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name='Impression Papier',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Papier',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Papier", )

            return impression_num_papiers(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_papiers(request, errors=1, errors_txt=errors)


def save_imp_object_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Objects_customForm1.Meta.fields}
            form = Objects_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Objects_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Objects_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(Service_name='Impression Objets',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Objets',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Objets", )

            return impression_num_objects(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_objects(request, errors=1, errors_txt=errors)

