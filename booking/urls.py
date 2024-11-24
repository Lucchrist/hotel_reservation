from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('recherche/', views.rechercher_reservation, name='recherche_reservation'),
 path('', views.index, name='index'),
    path('chambre/<int:chambre_id>/', views.details_chambre, name='details_chambre'),
    path('reservation/<int:chambre_id>/', views.faire_reservation, name='faire_reservation'),
    path('confirmation/<str:numero_reservation>/', views.confirmation_reservation, name='confirmation_reservation'),

    path('reservation/<int:chambre_id>/', views.faire_reservation, name='faire_reservation'),
    path('confirmation/<str:numero_reservation>/', views.confirmation_reservation, name='confirmation_reservation'),
]
