
from django.urls import path
from . import views

urlpatterns = [
path('agents', views.agents, name = 'agents'),
path('agents', views.agents, name = 'agents'),
path('register', views.register, name = 'register'),
path('login', views.user_login, name = 'login'),
path('logout', views.user_logout, name = 'logout'),
path('editagent', views.editagent, name = 'edit'),
path('updateagent/<str:id>', views.updateagent, name = 'update'),
path('deleteagents/<str:id>', views.deleteagents, name = 'delete'),



  # path('addagent', views.addagent, name = 'add'),
   # path('editfournisseur', views.editfournisseur, name = 'edit'),
   # path('updatefournisseur/<str:id>', views.updatefournisseur, name = 'update'),
   # path('deletefournisseur/<str:id>', views.deletefournisseur, name = 'delete'),
   


]