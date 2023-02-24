from django.db import models




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
    ('Direction de la coordination des services ratachés et des relations internationales', 'Direction de la coordination des services ratachés et des relations internationales'),
    ('Direction de l agence comptable du service de la comptabilité matière et du bureau de liaison à l etrnager', 'Direction de l agence comptable du service de la comptabilité matière et du bureau de liaison à l etrnager'),
    ('Direction de la legislation, du contrôle parlementaire et des services linguistique', 'Direction de la legislation, du contrôle parlementaire et des services linguistique'),
    ('Direction du budget et de la solde(DBS)', 'Direction du budget et de la solde(DBS)'),
    ('Direction des relations(DRH)', 'Direction des relations(DRH)'),
    ('Direction des actions sociales et médicales(DASM)', 'Direction des actions sociales et médicales(DASM)'),
    ('Direction des servides techniques commun(DSTC)', 'Direction des servides techniques commun(DSTC)'),
    ('Direction de la documentation, des archives et de la recherche parlementaire(DDARP)', 'Direction de la documentation, des archives et de la recherche parlementaire(DDARP)'),
    ('Inspecteurs généraux(IG)', 'Inspecteurs généraux(IG)'),
    ('Direction des relations(DRH)', 'Direction des relations(DRH)'),
    ('Sécrétaire particulier(SP)', 'Sécrétaire particulier(SP)'),
    ('Conseillé technique(CT)', 'Conseillé technique(CT)'),
    ('Chargé de mission(CM)', 'Chargé de mission(CM)'),
    ('Chargé d études(CE)', 'Chargé d études(CE)'),
    ('Chargé d études assistante(CE)', 'Chargé d études assistante(CE)'),
)

SERVICE_TRAITEMENT = (
    ('Direction de la coordination des services ratachés et des relations internationales', 'Direction de la coordination des services ratachés et des relations internationales'),
    ('Direction de l agence comptable du service de la comptabilité matière et du bureau de liaison à l etrnager', 'Direction de l agence comptable du service de la comptabilité matière et du bureau de liaison à l etrnager'),
    ('Direction de la legislation, du contrôle parlementaire et des services linguistique', 'Direction de la legislation, du contrôle parlementaire et des services linguistique'),
    ('Direction du budget et de la solde(DBS)', 'Direction du budget et de la solde(DBS)'),
    ('Direction des relations(DRH)', 'Direction des relations(DRH)'),
    ('Direction des actions sociales et médicales(DASM)', 'Direction des actions sociales et médicales(DASM)'),
    ('Direction des servides techniques commun(DSTC)', 'Direction des servides techniques commun(DSTC)'),
    ('Direction de la documentation, des archives et de la recherche parlementaire(DDARP)', 'Direction de la documentation, des archives et de la recherche parlementaire(DDARP)'),
    ('Inspecteurs généraux(IG)', 'Inspecteurs généraux(IG)'),
    ('Direction des relations(DRH)', 'Direction des relations(DRH)'),
    ('Sécrétaire particulier(SP)', 'Sécrétaire particulier(SP)'),
    ('Conseillé technique(CT)', 'Conseillé technique(CT)'),
    ('Chargé de mission(CM)', 'Chargé de mission(CM)'),
    ('Chargé d études(CE)', 'Chargé d études(CE)'),
    ('Chargé d études assistante(CE)', 'Chargé d études assistante(CE)'),
)

RECEPTEUR = (
    ('CABINET DU PRESIDENT DU SENAT', 'CABINET DU PRESIDENT DU SENAT'),
    ('SECRETARIAT GENERAL', 'SECRETARIAT GENERAL'),
    ('DECANT', 'DECANT'),
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
    date = models.DateField(blank=True, null=True)
    objet = models.CharField(max_length=10000, null=False, blank=False)

    service_traitement = models.CharField(max_length=150, choices=SERVICE_TRAITEMENT)
    mention = models.CharField(max_length=100, choices=MENTION, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.transmetteur}'

    class Meta:
        db_table = "courrier"