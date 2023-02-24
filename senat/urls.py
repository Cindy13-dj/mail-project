from django.urls import path
from . import views
from .views import *
# from .views import SearchResultsView
# from .views import SearchResultsList

app_name = "senat"

urlpatterns = [
    path('chef_service/', views.chef_service, name='chef_service'),
    path('chef_depart/', views.chef_depart, name='chef_depart'),
    path('chef_arrive/', views.chef_arrive, name='chef_arrive'),
    # path(r'^(?P<id>\d+)bureau_sg/$', views.bureau_sg, name='bureau_sg'),
    path('bureau_sg/', views.bureau_sg, name='bureau_sg'),
    path('usager/', views.usager, name='usager'),
    path('search/', views.search, name='search'),
    path('courrier_attente/', views.courrier_attente, name='courrier_attente'),
    path('<int:id>', views.courrier_attente_detail, name='courrier_attente_detail'),
    # path('traited/', views.traited, name='traited'),
    # path("search/", SearchResultsList.as_view(), name="search"),
    # path("search/", SearchResultsView.as_view(), name="search_results"),
    # path('sg_record/', sg_record, name='sg_record'),
]