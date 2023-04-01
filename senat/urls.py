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
    path('search_chef/', views.search_chef, name='search_chef'),
    path('result_chef/', views.result_chef, name='result_chef'),
    path('/', views.list_courrier, name='list_courrier'),
    path('df/<int:pk>/', views.courrier_pdf, name="courrier_pdf"),
    # path('traited/', views.traited, name='traited'),
    # path("search/", SearchResultsList.as_view(), name="search"),
    # path("search/", SearchResultsView.as_view(), name="search_results"),
    # path('sg_record/', sg_record, name='sg_record'),
    path('envoi_email/', views.envoi_email, name='envoi_email'),













    # path('inde/', views.inde, name='inde'),
    # path('capture/', views.capture, name='capture'),
    # path('save/', views.save_picture, name='save_picture'),

    # path('webcam/', views.webcam, name='webcam')
    # path('webcam/', views.webcam_capture, name='webcam'),
    path('inde/', views.webcam, name='webcam'),
    path('save_image/', views.save_image, name='save_image'),
    path('list/', views.webcam_list, name='webcam_list'),
]