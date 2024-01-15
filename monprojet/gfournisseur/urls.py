
from django.urls import path
from . import views

urlpatterns = [
    
    path('listesfourniseurs', views.listefournisseurs, name = 'fournisseurs'),
    path('addfournisseur', views.addfournisseur, name = 'add'),
   path('editfournisseur', views.editfournisseur, name = 'edit'),
    path('updatefournisseur/<str:id>', views.updatefournisseur, name = 'update'),
    path('deletefournisseur/<str:id>', views.deletefournisseur, name = 'delete'),

   

]