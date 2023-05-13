from django.db import models
from datetime import date




TYPES_COURRIERS = (
    ('LETTRE(L)', 'LETTRE(L)'),
    ('REQUETE(R)', 'REQUETE(R)'),
    ('LOI(LN)', 'LOI(LN)'),
    ('DECISION(D)', 'DECISION(D)'),
    ('NOTE(N)', 'NOTE(N)'),
    ('PROJET DE LOI(PJL)', 'PROJET DE LOI(PJL)'),
    ('PROPOSITION DE LOI(PL)', 'PROPOSITION DE LOI(PL)'),
    ('ARRETE DE BUREAU(AB)', 'ARRETE DE BUREAU(AB)'),
)

EMETTEUR = (
    ('Cabinet du président su Sénat(CABPSEN)', 'Cabinet du président su Sénat(CABPSEN)'),
    ('Sécrétaire Général(SG)', 'Sécrétaire Général(SG)'),
    ('Sécrétaire Général Adjoint 1(SGA1)', 'Sécrétaire Général Adjoint 1(SGA1)'),
    ('Sécrétaire Général Adjoint 2(SGA2)', 'Sécrétaire Général Adjoint 2(SGA2)'),
    ('Conseillé technique(CT)', 'Conseillé technique(CT)'),
    ('Chargé de mission(CM)', 'Chargé de mission(CM)'),
    ('Direction des missions internationales(DMI)', 'Direction des missions internationales(DMI)'),
    ('Direction des servides techniques commun(DSTC)', 'Direction des servides techniques commun(DSTC)'),
    ('Direction du budget de la solde(DBS)', 'Direction du budget de la solde(DBS)'),
    ('Direction agence comptable(AC)', 'Direction agence comptable(AC)'),
    ('Direction des actions sociales et médicales(DASM)', 'Direction des actions sociales et médicales(DASM)'),
    ("Direction de la traduction de l'interpretation(DTI)", "Direction de la traduction de l'interpretation(DTI)"),
    ('Direction de la coordination des services ratachés et des relations internationales', 'Direction de la coordination des services ratachés et des relations internationales'),
    ('Direction de la collectivité territorial décentralisées(DCTD)', 'Direction de la collectivité territorial décentralisées(DCTD)'),
    ('Direction des ressources humaines(DRH)', 'Direction des ressources humaines(DRH)'),
    ('Sercice du doyen', 'Sercice du doyen'),
    ('Sercice de la scolarité', 'Sercice de la scolarité'),
    ('Chef de département', 'Chef de département'),
    ('Sercice des questeurs', 'Sercice des questeurs'),
    ('AUTRES...', 'AUTRES...'),
)

SERVICE_TRAITEMENT = (
    ('Cabinet du président su Sénat(CABPSEN)', 'Cabinet du président su Sénat(CABPSEN)'),
    ('Sécrétaire Général(SG)', 'Sécrétaire Général(SG)'),
    ('Sécrétaire Général Adjoint 1(SGA1)', 'Sécrétaire Général Adjoint 1(SGA1)'),
    ('Sécrétaire Général Adjoint 2(SGA2)', 'Sécrétaire Général Adjoint 2(SGA2)'),
    ('Conseillé technique(CT)', 'Conseillé technique(CT)'),
    ('Chargé de mission(CM)', 'Chargé de mission(CM)'),
    ('Direction des missions internationales(DMI)', 'Direction des missions internationales(DMI)'),
    ('Direction des servides techniques commun(DSTC)', 'Direction des servides techniques commun(DSTC)'),
    ('Direction du budget de la solde(DBS)', 'Direction du budget de la solde(DBS)'),
    ('Direction agence comptable(AC)', 'Direction agence comptable(AC)'),
    ('Direction des actions sociales et médicales(DASM)', 'Direction des actions sociales et médicales(DASM)'),
    ("Direction de la traduction de l'interpretation(DTI)", "Direction de la traduction de l'interpretation(DTI)"),
    ('Direction de la coordination des services ratachés et des relations internationales', 'Direction de la coordination des services ratachés et des relations internationales'),
    ('Direction de la collectivité territorial décentralisées(DCTD)', 'Direction de la collectivité territorial décentralisées(DCTD)'),
    ('Direction des ressources humaines(DRH)', 'Direction des ressources humaines(DRH)'),
    ('Sercice du doyen', 'Sercice du doyen'),
    ('Sercice de la scolarité', 'Sercice de la scolarité'),
    ('Chef de département', 'Chef de département'),
    ('Sercice des questeurs', 'Sercice des questeurs'),
)

RECEPTEUR = (
    ('CABINET DU PRESIDENT DU SENAT', 'CABINET DU PRESIDENT DU SENAT'),
    ('SECRETARIAT GENERAL', 'SECRETARIAT GENERAL'),
    ('DECANAT', 'DECANAT'),
    ('Sercice des questeurs', 'Sercice des questeurs'),
)

STRUCTURE = (
    ('SENAT', 'SENAT'),
    ('UNIVERSITE DE YAOUNDE 1', 'UNIVERSITE DE YAOUNDE 1'),
)

MENTION = (
    ('ACCORD', 'ACCORD'),
    ('ETUDE ET COMPTE RENDU', 'ETUDE ET COMPTE RENDU'),
    ('ME VOIR', 'ME VOIR'),
    ('M EN PARLER', 'M EN PARLER'),
    ('REJET', 'REJET'),
    ('AUTRES', 'AUTRES'),
)

class Courrier(models.Model):
    transmetteur = models.CharField(max_length=150, choices=EMETTEUR)
    recepteur = models.CharField(max_length=100, choices=RECEPTEUR)
    types = models.CharField(max_length=100, choices=TYPES_COURRIERS)
    structure = models.CharField(max_length=100, choices=STRUCTURE, null=True, blank=True)
    code = models.CharField(max_length=100, null=False, blank=False)
    annee = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(blank=True, null=True, default=date.today)
    objet = models.CharField(max_length=10000, null=False, blank=False)

    service_traitement = models.CharField(max_length=150, choices=SERVICE_TRAITEMENT)
    mention = models.CharField(max_length=100, choices=MENTION, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transmetteur}'

    class Meta:
        db_table = "courrier"
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("Nous n'acceptons pas une date déjà passé!")
        return date
        if date > datetime.date.today():
            raise forms.ValidationError("Nous n'acceptons pas une date future!")
        return date



class Capture(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='captures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Scan(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='fichier', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name