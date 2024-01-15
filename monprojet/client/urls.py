
from django.urls import path
from . import views

urlpatterns = [
    
    path('listesclient', views.patient, name = 'clients'),
   path('addpatient', views.addpatient, name = 'addclient'),
    path('editpatient', views.editpatient, name = 'edit'),
    path('updatepatient/<str:id>', views.updatepatient, name = 'update'),
    path('deletepatient/<str:id>', views.deletepatient, name = 'delete'),
   

]