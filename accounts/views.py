from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from tablib import Dataset



def index(request):
    return render(request,'index.html')








def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            userSch = User.objects.get(email=email)
            print(userSch)
        except:
            userSch = None

        print(userSch)

        if userSch == None:
            messages.error(request, 'Utilisateur non trouvé !')
            return render(request, 'login.html')
        else:
            username = userSch.username
            user = authenticate(
                request, username=username, password=password)
        if user is not None and user.is_Chef_service:
            login(request, user)
            return redirect('senat:chef_service')
        elif user is not None and user.is_Chef_bureau_depart:
            login(request, user)
            return redirect('senat:chef_depart')
        elif user is not None and user.is_Chef_bureau_arrive:
            login(request, user)
            return redirect('senat:chef_arrive')
        elif user is not None and user.is_Secretaire_general:
            login(request, user)
            return redirect('senat:search')
        elif user is not None and user.is_Usager:
            login(request, user)
            return redirect('senat:usager')
        else:
            messages.error(request, 'Incorrect Email OR password')

    context = {}
    return render(request, 'login.html', context)
