from django.http import HttpResponse
from .models import vente, medicament

from datetime import date
from django.shortcuts import redirect, render
from .models import vente, medicament

def ajouter_vente(request):
    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        qte_achetee = request.POST.get('qte_achetee')

        # Récupérer les informations du médicament
        medicament_obj = medicament.objects.get(pk=medicament_id)
        prix_vente = medicament_obj.prix_vente
        date_expiration = medicament_obj.date_permeotion
        qte_en_stock = medicament_obj.qte

        # Conversion en entier
        qte_achetee = int(qte_achetee)
        qte_en_stock = int(qte_en_stock)

        # Calculer le prix total
        prix_total = float(prix_vente) * float(qte_achetee)

        # Vérifier si la quantité en stock est suffisante
        if qte_achetee <= qte_en_stock:
            # Mettre à jour la quantité en stock
            medicament_obj.qte -= qte_achetee
            medicament_obj.save()
            

            # Enregistrer la vente
            vente.objects.create(
                medicament=medicament_obj,
                quantite_vendue=qte_achetee,
                prix_total=prix_total,
                prix_rendu=0.0,
                reste_a_payer=0.0
            )
        
       
      
    ventes = vente.objects.all()  # Récupérer les ventes existantes
    medicaments = medicament.objects.all()
    return render(request, 'gventes/vente_form.html', {'medicaments': medicaments,'ventes': ventes})
          


#filtrer les ventes comprises entre les deux dates
from django.db.models import Q

def recherche_ventes(request):
    if request.method == 'GET':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        ventes = vente.objects.filter(
            Q(date_vente__gte=date_debut) & Q(date_vente__lte=date_fin)
        )

        context = {
            'ventes': ventes
        }

        return render(request, 'gventes/vente_form.html', context)
