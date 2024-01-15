from django.shortcuts import render, redirect

from .models import medicament, Facture, MedicamentsFacture,patients
from django.db.models import F



def creer_facture(request):

    pats = patients.objects.all()
    meds = medicament.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        date_facture= request.POST.get('date_facture')


        patient = patients.objects.get(pk=patient_id)
        facture = Facture.objects.create(patient=patient,date_facture=date_facture)

        medicament_id = request.POST.get('medicament')
        prix_vente = request.POST.get('prix_vente')

        quantite_stock = medicament.objects.get(pk=medicament_id).qte
        quantite_demandee = int(request.POST.get('quantite_demandee'))

        medicament_commande = MedicamentsFacture.objects.create(facture=facture,
                                                                medicament_id=medicament_id,
                                                                quantite_demandee=quantite_demandee,
                                                                )
        prix_total = float(prix_vente) * float( quantite_demandee)


        index = 1
        medicament_list = []  # Liste pour stocker les informations des médicaments supplémentaires
           
         #  
        while True:
            medicament_id = request.POST.get(f'medicament_{index}')

            if not medicament_id:
                break

            quantite_demandee = int(request.POST.get(f'quantite_demandee_{index}'))
            medicaments = medicament.objects.get(pk=medicament_id)

            medicament_facture = MedicamentsFacture.objects.create(facture=facture,
                                                            medicaments=medicaments,
                                                            quantite_demandee=quantite_demandee,
                                                            )

            medicament_list.append(medicament_commande)  # Ajouter l'objet MedicamentCommande à la liste


           
           
           
           
         #  
            index += 1

        return redirect('afficher_facture', facture_id=facture.id)

    return render(request, 'factures/creer_facture.html', { 'meds': meds,'pats':pats,})


#
def afficher_facture(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)
    medicaments_facture = MedicamentsFacture.objects.filter(facture=facture)
    medicament_list = []  # Liste pour stocker les médicaments supplémentaires

    # Calculer le prix total pour chaque médicament facturé
    for medicament_facture in medicaments_facture:
        medicament_facture.prix_total = medicament_facture.medicament.prix_vente * medicament_facture.quantite_demandee

    # Récupérer les informations des médicaments supplémentaires
    medicament_factures_supplementaires = MedicamentsFacture.objects.filter(facture=facture).exclude(id__in=medicaments_facture.values_list('id', flat=True))

    for medicament_facture in medicament_factures_supplementaires:
        medicament = medicament_facture.medicament
        quantite_demandee = medicament_facture.quantite_demandee

        medicament_info = {
            'medicament': medicament,
            'quantite_demandee': quantite_demandee,

        }
        medicament_list.append(medicament_info)

    total_prix = sum(medicament_facture.prix_total for medicament_facture in medicaments_facture)  # Calculer le prix total de la facture

    # annuler facture
    facture = Facture.objects.get(pk=facture_id)
    
    if request.method == 'POST' and 'annuler_facture' in request.POST:
        facture.annulee = True
        facture.save()
        return redirect('afficher_facture', facture_id=facture.id)
    


    return render(request,'factures/afficher_facture.html', {
        'facture': facture,
        'medicaments_facture': medicaments_facture,
        'medicament_list': medicament_list,
        'total_prix': total_prix,
    })
###

###

def ajouter_medicament(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)
    medicaments_facture = MedicamentsFacture.objects.filter(facture=facture)

    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        quantite_stock = medicament.objects.get(pk=medicament_id).qte
        quantite_demandee = int(request.POST.get('quantite_demandee'))

        medicament_facture = MedicamentsFacture.objects.create(facture=facture,
                                                                medicament_id=medicament_id,
                                                                quantite_demandee=quantite_demandee,
                                                                )

        return redirect('afficher_facture', facture_id=facture.id)

    meds = medicament.objects.all()
    return render(request, 'factures/ajouter_medicament.html', {'facture': facture, 'meds': meds})

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO


def imprimer_facture(request, facture_id):
    facture =Facture.objects.get(pk=facture_id)

###

    # Calculer le prix total pour chaque médicament facturé
    medicaments_facture = MedicamentsFacture.objects.filter(facture=facture)
    for medicament_facture in medicaments_facture:
        medicament_facture.prix_total = medicament_facture.medicament.prix_vente * medicament_facture.quantite_demandee


    # Calculer le prix total de la facture
    total_prix = sum(medicament_facture.prix_total for medicament_facture in medicaments_facture)

    


###
    # Récupérez les informations nécessaires pour générer le contenu de l'impression
    context = {
        'facture': facture,
        'medicaments_facture': medicaments_facture,
        'medicament_list': MedicamentsFacture.objects.filter(facture=facture).exclude(id__in=medicaments_facture.values_list('id', flat=True)),
        'total_prix': total_prix,
     }

    # Chargez le template d'impression
    template = get_template('factures/imprimer_facture.html')
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
    response['Content-Disposition'] = 'attachment; filename="facture.pdf"'

    # Écrivez le contenu PDF dans la réponse HTTP
    response.write(pdf)

    return response
   