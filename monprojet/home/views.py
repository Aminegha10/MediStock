from datetime import date
from itertools import count
from django.db.models import F
from gventes.models import vente
from django.db.models import Sum

from django.shortcuts import render
from gststock.models import medicament
from gfournisseur.models import fournisseur
from gcommande.models import gcommandes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
def is_gerant(user):
    return user.profile.grade == 'gerant'

@login_required

def index(request):
    return render(request,'home/index.html')
#permission
@login_required
@user_passes_test(is_gerant)
def menu(request):
 
 nombre_medicaments_expires = medicament.objects.filter(date_permeotion__lt=date.today()).count()
  
 frns = fournisseur.objects.all().count()
 
 cmd =gcommandes.objects.filter(annulee='False').order_by('-date_commande')[:3]  # Récupère les 5 derniers médicaments

 nombre_categories = medicament.objects.values('categorie').distinct().count()

 nombre_medicaments_rupture = medicament.objects.filter(qte__lte=F('stock_min')).count()


 ventes = vente.objects.values('medicament__designation', 'medicament__categorie').annotate(total_vendu=Sum('quantite_vendue')).order_by('-total_vendu')

 
 return render(request,'home/menu.html',{'frns': frns,'nombre_medicaments_expires':nombre_medicaments_expires,
                                         'cmd':cmd,'nombre_categories':nombre_categories,
                                        'nombre_medicaments_rupture':nombre_medicaments_rupture,
                                         'ventes':ventes }
                                         )



