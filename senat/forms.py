import datetime
from django.db import models
from django.http import request
from senat.models import *
from django import forms
from django.utils.safestring import mark_safe  # import pour mettre une url dans le help text


class RegistrationForm(forms.ModelForm):
    """ Formulaire pour la première phase d'enregistrement du Courrier """
    # Surchage de la classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Code qui permet de rendre obligatoire certains champs au niveau HTML
        for field in self.Meta.required:
            self.fields[field].required = True


    class Meta:

        model = Courrier
        fields = (
            'transmetteur', 'recepteur', 'code', 'date', 'objet', 'annee', 'structure', 'types'
        )
        widgets = {
            'transmetteur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Emetteur du courrier...',}),
            'recepteur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Recepteur du courrier...'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code du courrier...'}),
            'date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date de dépôt du courrier...'}),
            'annee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Année de dépôt du courrier...'}),
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet du courrier...'}),
            'structure': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Struture en charge du courrier...'}),
            'types': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type du courrier...'}),
        }

        required = (
            'code','objet', 'types'
        )
        
        help_texts = {
            'transmetteur':("Sélectionnez le transmetteur du courrier"), 
            'recepteur':("Sélectionnez le recepteur du courrier"), 
            'code':("Saisissez le code d'enregistrement du courrier Ex: 1"), 
            'date':("Saisissez la date d'enregistrement du courrier"), 
            'annee':("Saisissez l'année de dépôt du courrier"), 
            'objet':("Saisissez l'objet du courrier"),
            'structure':("Sélectionnez la structure en charge du courrier"),
            'types':("Sélectionnez le type du courrier"),
        }



class MentionForm(forms.ModelForm):
    """ Formulaire pour la deuxième phase d'enregistrement du Courrier """
    # Surchage de la classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Code qui permet de rendre obligatoire certains champs au niveau HTML
        for field in self.Meta.required:
            self.fields[field].required = True


    class Meta:

        model = Courrier
        fields = (
            'mention', 'service_traitement'
        )
        widgets = {
            'mention': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mention du courrier...',}),
            'service_traitement': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Service de traitement du courrier...'}),
        }

        required = (
            'mention','service_traitement'
        )
        
        help_texts = {
            'mention':("Sélectionnez la mention du courrier"), 
            'service_traitement':("Sélectionnez le service de traitement du courrier"), 
        }