from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from senat.forms import *
from datetime import datetime
import random
from .models import Courrier
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.db.models import Q # new
from django.views.generic import ListView
from django.urls import reverse
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from .utils import render_to_pdf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import CourrierFilter
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView







from django.forms import modelform_factory
# from .models import Picture

from django.core.files.storage import FileSystemStorage
# from .models import WebcamImage
from django.core.files.base import ContentFile
from django.utils import timezone
import re
from django.http import HttpResponseBadRequest




def chef_service(request):

    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    form = RegistrationForm(request.POST or None)
    chef_service = Courrier()

    if request.method == 'POST':
        # if code_unique:
        #     form = CiviliteForm(request.POST or None, instance=etudiant)
        #     if form.is_valid():
        #         form.save()
        #         messages.add_message(request, messages.SUCCESS, _(f"Informations de civilité modifiées avec succès."))
        #         return redirect('logement:filiation')
        #     else:
        #         messages.add_message(request, messages.ERROR, _('Veuillez vérifier les champs en rouge !!!'))
        #         return render(request, 'logement/civilite.html', {'form': form})
        # else:
        #     form = CiviliteForm(request.POST or None)
        #     etudiant = DemandeChambre()

        # form = RegistrationForm(request.POST or None)
        # chef_service = Courrier()

        if form.is_valid():
            # code_unique = generate_unique_code(str(form.cleaned_data['date_nais']))

            # etudiant.num_ordre = code_unique

            chef_service.transmetteur = form.cleaned_data['transmetteur']                
            chef_service.recepteur = form.cleaned_data['recepteur']                
            chef_service.code = form.cleaned_data['code']                
            chef_service.date = form.cleaned_data['date']                
            chef_service.objet = form.cleaned_data['objet']
            chef_service.structure = form.cleaned_data['structure']                
            chef_service.annee = form.cleaned_data['annee']
            chef_service.types = form.cleaned_data['types']
        
            chef_service.save()
            # request.session['code_logement'] = code_unique

            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))
            # return redirect('logement:filiation', request.session['ecole_code'] )
            return redirect('senat:chef_service')
        else:
            messages.add_message(request, messages.ERROR, ('Veuillez vérifier les champs en rouge !!!'))
            return render(request, 'chef_service.html', {'form': form})

    context = {
        'form': form,
        'count_courrier': count_courrier,
    }
    return render(request,'chef_service.html', context)



def chef_depart(request):
    return render(request,'chef_depart.html')



def chef_arrive(request):
    return render(request,'chef_arrive.html')



def bureau_sg(request):
    type_elt = request.GET.get('types')
    code = request.GET.get('code')

    # courrier = Courrier.objects.filter(
    #     Q(code__icontains=code) and Q(types__icontains=type_elt)
    # )
    courrier = Courrier.objects.filter(
        code=code, types=type_elt
    )
    # courriers = Courrier.objects.raw('select * from courrier where code="'+code+'" and types="'+type_elt+'"') 
    # if len(courriers) > 0:
    #     courrier = courriers.first()

    # sg = get_object_or_404(Courrier)
    # form = MentionForm(instance=sg)
    
    
    sg = get_object_or_404(Courrier, code=code, types=type_elt)
    form = MentionForm(instance=sg)

    # courrierss = MentionForm(request.POST or None, instance=code)
    if request.method == 'POST':
        form = MentionForm(request.POST or None, instance=sg)
        if form.is_valid():
            sg.service_traitement = form.cleaned_data['service_traitement']
            sg.mention = form.cleaned_data['mention']                
            # sg.service_traitement = form.cleaned_data['service_traitement'] 
            sg.save()
            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))
            # return redirect('senat:bureau_sg')

    return render(request,'sg.html', {"courrier": courrier, "form": form})



def usager(request):
    return render(request,'usager.html')



def search(request):
    
#     # clear_session(request)

#     # context = {}

#     # if request.method == 'POST':
#     #     code = request.POST['code']

#     #     if isinstance(code, str):
#     #         return redirect('senat:sg', code)
#     #     else:
#     #         messages.add_message(request, messages.ERROR, ('Mauvais format de code !!!'))
#     #         return render(request, 'search.html', {'code': code})

#     # return render(request, 'search.html', context)

#     # if request.method == 'GET':
#     #     query = request.GET.get('code')
#     #     if query:
#     #         courrier = Courrier.objects.filter(code__icontains=query) 
#     #         return render(request, 'sg.html', {'courrier':courrier})
#     #     else:
#     #         # messages.add_message(request, messages.ERROR, ('Mauvais format de code !!!'))
#     #         return render(request, 'search.html', {})

#     # if request.method == 'GET':
#     #     query = request.GET.get('code')
#     #     querys = request.GET.get('types')
#     #     if query:
#     #         courrier = Courrier.objects.raw('select * from courrier where code="'+query+'" and types="'+querys+'"') 
#     #         return render(request, 'sg.html', {'courrier':courrier})
#     #     else:
#     #         # messages.add_message(request, messages.ERROR, ('Mauvais format de code !!!'))
#     #         return render(request, 'search.html', {})

    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        # courrier = Courrier.objects.raw('select * from courrier where code="'+query+'" and types="'+querys+'"') 


        # if not query or not querys:
        #     messages.error(request, 'Vous devez renseigner ls champs.')
        # return redirect('senat:search')

        objects = Courrier.objects.filter(code=query, types=querys, structure="SENAT")
        if not objects: 
            messages.error(request, "Le code ou le type fourni n'existe pas")
            return redirect('senat:search')


        response = redirect('/bureau_sg/' + f'?code={query}&types={querys}')
        # messages.add_message(request, messages.ERROR, ('Mauvais format de code !!!'))
        return response

        # return redirect('senat:bureau_sg', kwargs={'courrier':courrier})
        # return render(request, 'sg.html', {'courrier':courrier})
        # return redirect(f'senat:bureau_sg/?query={query}/?querys={querys}')
        # return redirect('senat:bureau_sg')
    else:
        # messages.add_message(request, messages.ERROR, ('Mauvais format de code !!!'))
        return render(request, 'search.html')



def bureau_univ(request):
    type_elt = request.GET.get('types')
    code = request.GET.get('code')
    courrier = Courrier.objects.filter(
        code=code, types=type_elt
    )
    sg = get_object_or_404(Courrier, code=code, types=type_elt)
    form = MentionForm(instance=sg)

    if request.method == 'POST':
        form = MentionForm(request.POST or None, instance=sg)
        if form.is_valid():
            sg.service_traitement = form.cleaned_data['service_traitement']
            sg.mention = form.cleaned_data['mention']                
            
            sg.save()
            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))

    return render(request,'univ.html', {"courrier": courrier, "form": form})


def search_univ(request):

    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        

        objects = Courrier.objects.filter(code=query, types=querys, structure="UNIVERSITE DE YAOUNDE 1")
        if not objects: 
            messages.error(request, "Le code ou le type fourni n'existe pas")
            return redirect('senat:search_univ')
        response = redirect('/bureau_univ/' + f'?code={query}&types={querys}')
        return response
    else:
        return render(request, 'search_univ.html')



def courrier_attente(request):
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    # if request.method == 'POST':
    #     request.is_active = False
    #     request.save()
    return render(request, 'courrier_attente.html', {"courrier": courrier})



def deactivate_record(request, id):
    record = get_object_or_404(Courrier, pk=id)
    if request.method == 'POST':
        record.is_active = False
        record.save()
        return HttpResponseRedirect('/')
    return render(request, 'chef_service.html', {"record": record})



def courrier_attente_detail(request, id):
    obj = get_object_or_404(Courrier, pk=id)

    #compter le nombre de courrier
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    return render(request, 'courrier_detail.html', {"obj": obj, "count_courrier": count_courrier})



# def traited(request):
#     is_active = False
#     request.object.save()
#     return redirect('senat:courrier_attente')



def search_chef(request):

    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        queryss = request.POST.get('objet')


        response = redirect('/result_chef/' + f'?code={query}&types={querys}&objet={queryss}' or f'?code={query}&types={querys}&objet={queryss}' or f'?objet={queryss}')
        return response
    else:
        return render(request, 'search_chef.html')



def result_chef(request):
     #compter le nombre de courrier
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    type_elt = request.GET.get('types')
    code = request.GET.get('code')
    objet = request.GET.get('objet')



    courrier = Courrier.objects.filter(
        code=code, types=type_elt
    ) or Courrier.objects.filter(
        code=code, types=type_elt, objet=objet
    )or Courrier.objects.filter(
        objet=objet
    )
    return render(request,'result_chef.html', {"courrier": courrier, "count_courrier": count_courrier})



def courrier_pdf(request, pk):
    user_courrier = Courrier.objects.get(pk=pk)

    context = {
        "user_courrier": user_courrier,
    }
    
    pdf = render_to_pdf('courrier_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')



def list_courrier(request):
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    courriers = Courrier.objects.all()
    # courriers = Courrier.objects.filter(is_active=True).order_by('-created_on')

    #pagination
    # page = request.GET.get('page')
    # num_of_items = 3
    # paginator = Paginator(courriers, num_of_items)

    # try:
    #     courrierss = paginator.page(page)
    # except PageNotAnInteger:
    #     page = 1
    #     courrierss = paginator.page(page)
    # except EmptyPage:
    #     page = paginator.num_pages
    #     courrierss = paginator.page(page)

    #barre de filtre
    courriers_filter = CourrierFilter(request.GET, queryset=courriers)

    return render(request, 'liste_courrier.html', {'courriers': courriers, 
                                                   'count_courrier': count_courrier, 
                                                #    'paginator': paginator,
                                                   'courriers_filter':courriers_filter,
                                                   })



def envoi_email(request):
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        # phone = request.POST.get('phone')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')
        form_data = {
            'name':name,
            'email':email,
            # 'phone':phone,
            'message':message,
            'attachment':MIMEMultipart(),
        }
        recipient_list = email
        # message = '''
        # From:\n\t\t{}\n
        # Message:\n\t\t{}\n
        # Email:\n\t\t{}\n
        
        
        
        # '''.format(form_data['name'], form_data['message'], form_data['email'])
        # send_mail('You got a mail!', message, '', ['ngounouloic853@gmail.com']) # TODO: enter your email address
        send_mail(name, message, email, [recipient_list], attachment)
        

    return render(request,'envoi_email.html', {"courrier": courrier, "count_courrier": count_courrier})








import base64
import io
import numpy as np
import cv2
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Capture
from io import BytesIO
from django.utils.encoding import smart_str
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def indexs(request):
    return render(request, 'indexs.html')



# def capture(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         image_data = request.POST.get('image')
#         image_data = image_data.replace('data:image/png;base64,', '')
#         image_data = base64.b64decode(image_data)
#         capture = Capture(name=name)
#         image_file = BytesIO(image_data)
#         capture.image.save(name + '.png', image_file)
#         capture.save()
#         return redirect('senat:captures')
#     return render(request, 'capture.html')



def captures(request):
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    captures = Scan.objects.all()
    return render(request, 'captures.html', {'captures': captures, 'count_courrier':count_courrier})










def scan(request):

    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    form = ScanForm(request.POST, request.FILES)
    scan = Scan()

    if request.method == 'POST':
        if form.is_valid():
            scan.name = form.cleaned_data['name']                
            scan.file = form.cleaned_data['file']                
        
            scan.save()
            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))
            return redirect('senat:scan')
        else:
            messages.add_message(request, messages.ERROR, ('Veuillez vérifier les champs !!!'))
            return render(request, 'scan.html', {'form': form})
    context = {
        'form': form,
        'count_courrier': count_courrier,
    }
    return render(request,'scan.html', context)







def download_capture(request, capture_id):
    capture = get_object_or_404(Scan, id=capture_id)
    response = HttpResponse(capture.file, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename={}'.format(smart_str(capture.name + '.png'))
    return response

def download_capture_pdf(request, capture_id):
    capture = get_object_or_404(Scan, id=capture_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={}'.format(smart_str(capture.name + '.pdf'))
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    img = ImageReader(capture.file.path)
    pdf.drawImage(img, 0, 0, width=letter[0], height=letter[1])
    pdf.showPage()
    pdf.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    response.write(pdf_data)
    return response