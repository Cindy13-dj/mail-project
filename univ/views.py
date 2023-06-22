from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from univ.forms import *
from datetime import datetime
import random
from .models import Courrier_Univ
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




def chef_univ(request):

    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    form = RegistrationForm(request.POST or None)
    chef_univ = Courrier_Univ()

    if request.method == 'POST':

        if form.is_valid():

            chef_univ.transmetteur = form.cleaned_data['transmetteur']                
            chef_univ.recepteur = form.cleaned_data['recepteur']                
            chef_univ.code = form.cleaned_data['code']                
            chef_univ.date = form.cleaned_data['date']                
            chef_univ.objet = form.cleaned_data['objet']
            chef_univ.structure = form.cleaned_data['structure']                
            chef_univ.annee = form.cleaned_data['annee']
            chef_univ.types = form.cleaned_data['types']
        
            chef_univ.save()

            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))
            return redirect('univ:chef_univ')
        else:
            messages.add_message(request, messages.ERROR, ('Veuillez vérifier les champs en rouge !!!'))
            return render(request, 'univ/chef_univ.html', {'form': form})

    context = {
        'form': form,
        'count_courrier': count_courrier,
    }
    return render(request,'univ/chef_univ.html', context)



def bureau_univ(request):
    type_elt = request.GET.get('types')
    code = request.GET.get('code')
    courrier = Courrier_Univ.objects.filter(
        code=code, types=type_elt
    )
    sg = get_object_or_404(Courrier_Univ, code=code, types=type_elt)
    form = MentionForm(instance=sg)

    if request.method == 'POST':
        form = MentionForm(request.POST or None, instance=sg)
        if form.is_valid():
            sg.service_traitement = form.cleaned_data['service_traitement']
            sg.mention = form.cleaned_data['mention']                
            
            sg.save()
            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))

    return render(request,'univ/univ.html', {"courrier": courrier, "form": form})


def search_univ(request):

    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        

        objects = Courrier_Univ.objects.filter(code=query, types=querys, structure="UNIVERSITE DE YAOUNDE 1")
        if not objects: 
            messages.error(request, "Le code ou le type fourni n'existe pas")
            return redirect('univ:search_univ')
        response = redirect('/univ/bureau_univ/' + f'?code={query}&types={querys}')
        return response
    else:
        return render(request, 'univ/search_univ.html')



def courrier_attente(request):
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    # if request.method == 'POST':
    #     request.is_active = False
    #     request.save()
    return render(request, 'univ/courrier_attente.html', {"courrier": courrier})



def deactivate_record(request, id):
    record = get_object_or_404(Courrier_Univ, pk=id)
    if request.method == 'POST':
        record.is_active = False
        record.save()
        return HttpResponseRedirect('/')
    return render(request, 'univ/chef_univ.html', {"record": record})



def courrier_attente_detail(request, id):
    obj = get_object_or_404(Courrier_Univ, pk=id)

    #compter le nombre de courrier
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    return render(request, 'univ/courrier_detail.html', {"obj": obj, "count_courrier": count_courrier})



# def traited(request):
#     is_active = False
#     request.object.save()
#     return redirect('senat:courrier_attente')



def search_chef(request):

    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        queryss = request.POST.get('objet')


        response = redirect('/univ/result_chef/' + f'?code={query}&types={querys}&objet={queryss}' or f'?code={query}&types={querys}&objet={queryss}' or f'?objet={queryss}')
        return response
    else:
        return render(request, 'univ/search_chef.html')



def result_chef(request):
     #compter le nombre de courrier
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    type_elt = request.GET.get('types')
    code = request.GET.get('code')
    objet = request.GET.get('objet')



    courrier = Courrier_Univ.objects.filter(
        code=code, types=type_elt
    ) or Courrier_Univ.objects.filter(
        code=code, types=type_elt, objet=objet
    )or Courrier_Univ.objects.filter(
        objet=objet
    )
    return render(request,'univ/result_chef.html', {"courrier": courrier, "count_courrier": count_courrier})



def courrier_pdf(request, pk):
    user_courrier = Courrier_Univ.objects.get(pk=pk)

    context = {
        "user_courrier": user_courrier,
    }
    
    pdf = render_to_pdf('univ/courrier_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')



def list_courrier(request):
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    courriers = Courrier_Univ.objects.all()
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

    return render(request, 'univ/liste_courrier.html', {'courriers': courriers, 
                                                   'count_courrier': count_courrier, 
                                                #    'paginator': paginator,
                                                   'courriers_filter':courriers_filter,
                                                   })



def envoi_email(request):
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
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
        

    return render(request,'univ/envoi_email.html', {"courrier": courrier, "count_courrier": count_courrier})








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
    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    captures = Scan_Univ.objects.all()
    return render(request, 'univ/captures.html', {'captures': captures, 'count_courrier':count_courrier})










def scan(request):

    courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    count_courrier = courrier.count()

    form = ScanForm(request.POST, request.FILES)
    scan = Scan_Univ()

    if request.method == 'POST':
        if form.is_valid():
            scan.name = form.cleaned_data['name']                
            scan.file = form.cleaned_data['file']                
        
            scan.save()
            messages.add_message(request, messages.SUCCESS, (f"Informations du courrier enregistrées avec succès."))
            return redirect('univ:scan')
        else:
            messages.add_message(request, messages.ERROR, ('Veuillez vérifier les champs !!!'))
            return render(request, 'univ/scan.html', {'form': form})
    context = {
        'form': form,
        'count_courrier': count_courrier,
    }
    return render(request,'univ/scan.html', context)







def download_capture(request, capture_id):
    capture = get_object_or_404(Scan_Univ, id=capture_id)
    response = HttpResponse(capture.file, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename={}'.format(smart_str(capture.name + '.png'))
    return response

def download_capture_pdf(request, capture_id):
    capture = get_object_or_404(Scan_Univ, id=capture_id)
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












def search_usager(request):
    
    if request.method == 'POST':
        query = request.POST.get('code')
        querys = request.POST.get('types')
        queryss = request.POST.get('objet')


        response = redirect('/univ/result_usager/' + f'?code={query}&types={querys}&objet={queryss}' or f'?code={query}&types={querys}&objet={queryss}' or f'?objet={queryss}')
        return response
    else:
        return render(request, 'univ/search_usager.html')



def result_usager(request):
     #compter le nombre de courrier
    # courrier = Courrier_Univ.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    # count_courrier = courrier.count()

    type_elt = request.GET.get('types')
    code = request.GET.get('code')
    objet = request.GET.get('objet')



    courrier = Courrier_Univ.objects.filter(
        code=code, types=type_elt
    ) or Courrier_Univ.objects.filter(
        code=code, types=type_elt, objet=objet
    )or Courrier_Univ.objects.filter(
        objet=objet
    )
    return render(request,'univ/result_usager.html', {"courrier": courrier})