from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import medicament, gcommandes, MedicamentsCommande,fournisseur
from django.db.models import F


def is_gerant(user):
    return user.profile.grade == 'gerant'

@login_required
@user_passes_test(is_gerant)
def creer_commande(request):

    frns = fournisseur.objects.all()
    meds = medicament.objects.all()

    if request.method == 'POST':
        fournisseur_id = request.POST.get('fournisseur')
        adresse_livraison = request.POST.get('adresse_livraison')
        date_commande= request.POST.get('date_commande')


        fourniseur = fournisseur.objects.get(pk=fournisseur_id)
        commande = gcommandes.objects.create(fournisseur=fourniseur, adresse_livraison=adresse_livraison,date_commande=date_commande)

        medicament_id = request.POST.get('medicament')
        quantite_stock = medicament.objects.get(pk=medicament_id).qte
        quantite_demandee = int(request.POST.get('quantite_demandee'))
        description = request.POST.get('description')

        medicament_commande = MedicamentsCommande.objects.create(commande=commande,
                                                                medicament_id=medicament_id,
                                                                quantite_demandee=quantite_demandee,
                                                                description=description)

        index = 1
        medicament_list = []  # Liste pour stocker les informations des médicaments supplémentaires
           
         #  
        while True:
            medicament_id = request.POST.get(f'medicament_{index}')

            if not medicament_id:
                break

            quantite_demandee = int(request.POST.get(f'quantite_demandee_{index}'))
            description = request.POST.get(f'description_{index}')
            medicaments = medicament.objects.get(pk=medicament_id)

            medicament_commande = MedicamentsCommande.objects.create(commande=commande,
                                                            medicaments=medicaments,
                                                            quantite_demandee=quantite_demandee,
                                                            description=description)

            medicament_list.append(medicament_commande)  # Ajouter l'objet MedicamentCommande à la liste


           
           
           
           
         #  
            index += 1

        return redirect('afficher_commande', commande_id=commande.id)
    medicaments_rupture = medicament.objects.filter(qte__lte=F('stock_min'))

    return render(request, 'gcommande/creer_commande.html', { 'meds': meds,'frns':frns,
                                                             'medicaments_rupture':medicaments_rupture})
@user_passes_test(is_gerant)

def afficher_commande(request, commande_id):
    commande = gcommandes.objects.get(pk=commande_id)
    medicaments_commande = MedicamentsCommande.objects.filter(commande=commande)
    medicament_list = []  # Liste pour stocker les médicaments supplémentaires

    # Récupérer les informations des médicaments supplémentaires
    medicament_commandes_supplementaires = MedicamentsCommande.objects.filter(commande=commande).exclude(id__in=medicaments_commande.values_list('id', flat=True))
    
    for medicament_commande in medicament_commandes_supplementaires:
        medicament = medicament_commande.medicament
        quantite_demandee = medicament_commande.quantite_demandee
        description = medicament_commande.description

        medicament_info = {
            'medicament': medicament,
            'quantite_demandee': quantite_demandee,
            'description': description
        }
        medicament_list.append(medicament_info)
        #
        
        # annuler commande
    commande = gcommandes.objects.get(pk=commande_id)
    
    if request.method == 'POST' and 'annuler_commande' in request.POST:
        commande.annulee = True
        commande.save()
        return redirect('afficher_commande', commande_id=commande.id)
    

#


    return render(request, 'gcommande/afficher_commande.html', {'commande': commande,
                                                                'medicaments_commande': medicaments_commande,
                                                                'medicament_list': medicament_list})


@user_passes_test(is_gerant)

def ajouter_medicament(request, commande_id):
    commande = gcommandes.objects.get(pk=commande_id)
    medicaments_commande = MedicamentsCommande.objects.filter(commande=commande)

    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        quantite_stock = medicament.objects.get(pk=medicament_id).qte
        quantite_demandee = int(request.POST.get('quantite_demandee'))
        description = request.POST.get('description')

        medicament_commande = MedicamentsCommande.objects.create(commande=commande,
                                                                medicament_id=medicament_id,
                                                                quantite_demandee=quantite_demandee,
                                                                description=description)

        return redirect('afficher_commande', commande_id=commande.id)

    meds = medicament.objects.all()
    return render(request, 'gcommande/ajouter_medicament.html', {'commande': commande, 'meds': meds})

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

@user_passes_test(is_gerant)

def imprimer_commande(request, commande_id):
    commande = gcommandes.objects.get(pk=commande_id)

    # Récupérez les informations nécessaires pour générer le contenu de l'impression
    context = {
        'commande': commande,
        'medicaments_commande': MedicamentsCommande.objects.filter(commande=commande),
        'medicament_list': MedicamentsCommande.objects.filter(commande=commande).exclude(id__in=MedicamentsCommande.objects.filter(commande=commande).values_list('id', flat=True))
    }

    # Chargez le template d'impression
    template = get_template('gcommande/imprimer_commande.html')
    content = template.render(context)

    # Créez un flux de données pour stocker le résultat PDF
    pdf_file = BytesIO()

    # Convertissez le contenu HTML en PDF
    pisa.CreatePDF(content, dest=pdf_file)

    # Récupérez le contenu du fichier PDF à partir du flux de données
    pdf = pdf_file.getvalue()

    # Fermez le flux de données
    pdf_file.close()

    # Créez une réponse HTTP avec le contenu du PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="commande.pdf"'

    # Écrivez le contenu PDF dans la réponse HTTP
    response.write(pdf)

    return response


def tout_commandes(request):
 cmd =gcommandes.objects.all().filter(annulee='False')
       
 context = {'cmd': cmd}
 return render(request, 'gcommande/tout_commandes.html',context)
 

from math import sqrt

def calcul_quantite_optimale(request):
    if request.method == 'POST':
        demande_annuelle = float(request.POST['demande_annuelle'])
        cout_stock = float(request.POST['cout_stock'])
        cout_commande = float(request.POST['cout_commande'])

        quantite_optimale = round(sqrt((2 * demande_annuelle * cout_commande) / cout_stock))

        return render(request, 'resultat_quantite_optimale.html', {'quantite_optimale': quantite_optimale})

    return render(request, 'calcul_quantite_optimale.html')
