from django.contrib import admin
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.shortcuts import render

# from utils.functions import send_mail
from .models import User
from .resources import UserResource
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import Group
import shortuuid



class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(ImportExportModelAdmin):
    list_display = (
        'username',
        'last_name',  
        'email', 
        'is_Chef_service', 
        'is_Chef_bureau_depart', 
        'is_Chef_bureau_arrive',
        'is_Secretaire_general',
        'is_Usager'
    )


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
    
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Fichier invalide')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                print('sdc')
                print(x)
                fields = x.split(";")
                print(fields)

                pass_word = fields[0]
                if pass_word == "":
                    pass_word = shortuuid.ShortUUID().random(length=8)
                
                hashed_pwd = make_password(pass_word)
                # check_password(fields[0],hashed_pwd)
                try:
                    created = User.objects.update_or_create(
                        password = hashed_pwd,
                        username = fields[1],
                        first_name = fields[2],
                        last_name = fields[3],
                        phone = fields[4],
                        # is_Chef_bureau_arrive = fields[5],
                        email = fields[5],
                    )

                    print(f"{fields[-1]}")

                    
                except:
                    print("Erreur lors de la creation du compte")
                 


            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


    # def upload_csv(self, request):
    
    #     if request.method == "POST":
    #         csv_file = request.FILES["csv_upload"]
            
    #         if not csv_file.name.endswith('.csv'):
    #             messages.warning(request, 'The wrong file type was uploaded')
    #             return HttpResponseRedirect(request.path_info)
            
    #         file_data = csv_file.read().decode("utf-8")
    #         csv_data = file_data.split("\n")

    #         for x in csv_data:
    #             fields = x.split(",")
    #             created = customer.objects.update_or_create(
    #                 name = fields[0],
    #                 balance = fields[1],
    #                 )
    #         url = reverse('admin:index')
    #         return HttpResponseRedirect(url)

    #     form = CsvImportForm()
    #     data = {"form": form}
    #     return render(request, "admin/csv_upload.html", data)



admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)