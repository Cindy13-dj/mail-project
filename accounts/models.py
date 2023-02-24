from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_Chef_service= models.BooleanField('Is Chef Service', default=False)
    is_Chef_bureau_depart= models.BooleanField('Is Chef bureau depart', default=False)
    is_Chef_bureau_arrive= models.BooleanField('Is Chef bureau arrive', default=False)
    is_Secretaire_general= models.BooleanField('Is Secretaire general', default=False)
    is_Usager = models.BooleanField('Is Usager', default=False)
    phone = models.CharField(max_length=9)