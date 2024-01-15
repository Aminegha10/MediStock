
from django.urls import path
from . import views

    
urlpatterns = [
   path('creer_facture/',views.creer_facture, name='creer_facture'),
  path('afficher_facture/<int:facture_id>/',views.afficher_facture, name='afficher_facture'),
 path('facture/ajouter_medicament/<int:facture_id>/', views.ajouter_medicament, name='ajouter_medicament'),

  path('facture/imprimer/<int:facture_id>/', views.imprimer_facture, name='imprimer_facture'),

    
]
   
