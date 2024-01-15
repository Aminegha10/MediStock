from django.urls import path
from .views import ajouter_vente, recherche_ventes

urlpatterns = [
    path('vente/ajouter/', ajouter_vente, name='ajouter_vente'),
    path('recherche-ventes/',recherche_ventes, name='recherche_ventes'),
]


