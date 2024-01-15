
from django.urls import path
from . import views

    
urlpatterns = [
   path('creer_commande/',views.creer_commande, name='creer_commande'),
  path('afficher_commande/<int:commande_id>/',views.afficher_commande, name='afficher_commande'),
 path('commande/ajouter_medicament/<int:commande_id>/', views.ajouter_medicament, name='ajouter_medicament'),

   path('commande/imprimer/<int:commande_id>/', views.imprimer_commande, name='imprimer_commande'),

       path('tout_commandes/', views.tout_commandes, name='tout_commandes'),
           path('calcul_quantite_optimale', views.calcul_quantite_optimale, name='calcul_quantite_optimale'),


]
   


