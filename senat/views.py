from django.shortcuts import render, redirect
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
            sg.mention = form.cleaned_data['mention']                
            sg.service_traitement = form.cleaned_data['service_traitement'] 
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



def courrier_attente(request):
    courrier = Courrier.objects.filter(mention="ETUDE ET COMPTE RENDU", is_active=True)
    # if request.method == 'POST':
    #     request.is_active = False
    #     request.save()
    return render(request, 'courrier_attente.html', {"courrier": courrier})



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