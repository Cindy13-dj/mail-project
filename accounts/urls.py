from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    # path('chef_service/', views.chef_service, name='chef_service'),
    # path('chef_depart/', views.chef_depart, name='chef_depart'),
    # path('chef_arrive/', views.chef_arrive, name='chef_arrive'),
    # path('sg/', views.sg, name='sg'),
    # path('usager/', views.usager, name='usager'),
]