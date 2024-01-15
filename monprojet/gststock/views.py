from datetime import date, timedelta
from django.db.models import F, Q
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import medicament
# Create your views here.
@login_required

def stock(request):
  
    if 'q' in request.GET:
       q = request.GET['q']
       meds = medicament.objects.filter(designation__icontains=q)
       context = {
        'meds':meds,
    }
    else:
       meds = medicament.objects.all()
       
    context = {'meds': meds}
    return render(request, 'gstock/stock.html', context)

def filtre_date(request):
    meds=medicament.objects.filter(date_permeotion__lt=date.today())
    
    context = {'meds': meds}
    return render(request, 'gstock/stock.html', context)

def filtre_qte(request):
    meds = medicament.objects.filter(qte__lte=F('stock_min'))
    context = {'meds': meds}
    return render(request, 'gstock/stock.html', context)

def order_by_categorie(request):
    meds = medicament.objects.all().order_by('categorie')
    context = {'meds': meds}
    return render(request, 'gstock/stock.html', context)

def order_by_designation(request):
    meds = medicament.objects.all().order_by('designation')
    context = {'meds': meds}
    return render(request, 'gstock/stock.html', context)

def addstock(request):
    if request.method == "POST" :
      cb = request.POST.get('cb')
      Designation = request.POST.get('Designation')
      Categorie = request.POST.get('Categorie')
      Forme = request.POST.get('Forme')
      dci = request.POST.get('DCI')
      qte = request.POST.get('qte')
      pv = request.POST.get('pv')
      dz = request.POST.get('dz')
      pa = request.POST.get('pa')
      sm = request.POST.get('sm')
      dp = request.POST.get('dp')
      lieustock = request.POST.get('lieustock')
      data = medicament (
         CodeBarre = cb ,
    designation = Designation,
    categorie = Categorie,
    forme = Forme,
    DCI= dci,
    qte = qte,
    dosage = dz,
    prix_vente =pv,
    stock_min = sm,
    prix_achat =pa,
    date_permeotion = dp,
    lieu_med = lieustock
      )
      data.save()
      
      return redirect('stock')
    return render(request,'gstock/stock.html')


def editstock(request):
 meds = medicament.objects.all()
 context = {
    'meds':meds,
 }

 return redirect(request,'gstock/stock.html',context)

def updatestock(request,id):
   if request.method == "POST" :
     cb = request.POST.get('cb')
     Designation = request.POST.get('Designation')
     Categorie = request.POST.get('Categorie')
     Forme = request.POST.get('Forme')
     dci = request.POST.get('DCI')
     qte = request.POST.get('qte')
     pv = request.POST.get('pv')
     dz = request.POST.get('dz')
     pa = request.POST.get('pa')
     sm = request.POST.get('sm')
     dp = request.POST.get('dp')
     lieustock = request.POST.get('lieustock')
     data = medicament (
        id = id,
        CodeBarre = cb ,
        designation = Designation,
         categorie = Categorie,
          forme = Forme,
         DCI= dci,
         qte = qte,
         dosage = dz,
         prix_vente =pv,
         stock_min = sm,
          prix_achat =pa,
         date_permeotion =dp,
           lieu_med = lieustock
                        )
     data.save()
     return redirect('stock')
   return redirect(request,'gstock/stock.html')
def delete(request,id):
       meds = medicament.objects.filter(id = id)
       meds.delete()
       context = {
        'meds':meds,
    }
       return redirect('stock')


from django.db.models import F
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import medicament, Notification

@login_required
def notifications_ajax(request):
    user = request.user

    # Mettre à jour les notifications pour les ruptures de stock et les médicaments périmés
    stock_notifications = medicament.objects.filter(qte__lte=F('stock_min'), date_permeotion__lt=date.today()).values('id', 'designation')
    for stock_notification in stock_notifications:
        medicament_id = stock_notification['id']
        designation = stock_notification['designation']
        notification = Notification.objects.filter(user=user, medicament_lien_id=medicament_id, is_read=False).first()
        if notification:
            if notification.title != 'Rupture de stock et médicament périmé':
                notification.title = 'Rupture de stock et médicament périmé'
                notification.message = f"Le médicament {designation} est en rupture de stock et périmé."
                notification.save()
        else:
            notification = Notification(
                user=user,
                medicament_lien_id=medicament_id,
                title='Rupture de stock et médicament périmé',
                message=f"Le médicament {designation} est en rupture de stock et périmé.",
                url='/medicament/' + str(medicament_id)
            )
            notification.save()

    # Mettre à jour les notifications pour les ruptures de stock uniquement
    stock_only_notifications = medicament.objects.filter(qte__lte=F('stock_min'), date_permeotion__gte=date.today()).values('id', 'designation')
    for stock_only_notification in stock_only_notifications:
        medicament_id = stock_only_notification['id']
        designation = stock_only_notification['designation']
        notification = Notification.objects.filter(user=user, medicament_lien_id=medicament_id, is_read=False).first()
        if notification:
            if notification.title != 'Rupture de stock':
                notification.title = 'Rupture de stock'
                notification.message = f"Le médicament {designation} est en rupture de stock."
                notification.save()
        else:
            notification = Notification(
                user=user,
                medicament_lien_id=medicament_id,
                title='Rupture de stock',
                message=f"Le médicament {designation} est en rupture de stock.",
                url='/medicament/' + str(medicament_id)
            )
            notification.save()

    # Mettre à jour les notifications pour les médicaments périmés uniquement
    peremption_notifications = medicament.objects.filter(date_permeotion__lt=date.today(), qte__gt=F('stock_min')).values('id', 'designation')
    for peremption_notification in peremption_notifications:
        medicament_id = peremption_notification['id']
        designation = peremption_notification['designation']
        notification = Notification.objects.filter(user=user, medicament_lien_id=medicament_id, is_read=False).first()
        if notification:
            if notification.title != 'Médicament périmé':
                notification.title = 'Médicament périmé'
                notification.message = f"Le médicament {designation} est périmé."
                notification.save()
        else:
            notification = Notification(
                user=user,
                medicament_lien_id=medicament_id,
                title='Médicament périmé',
                message=f"Le médicament {designation} est périmé.",
                url='/medicament/' + str(medicament_id)
            )
            notification.save()
            ##3
       

   
     # Mettre à jour les notifications pour les médicaments approchant de la date de péremption
    expiration_date = date.today() + timedelta(days=90)  # Date limite de 3 mois
    peremption_notifications = medicament.objects.filter(date_permeotion__gt=date.today(), date_permeotion__lte=expiration_date, qte__gt=F('stock_min')).values('id', 'designation')
    for peremption_notification in peremption_notifications:
        medicament_id = peremption_notification['id']
        designation = peremption_notification['designation']
        notification = Notification.objects.filter(user=user, medicament_lien_id=medicament_id, is_read=False).first()
        if notification:
            if notification.title != 'Médicament approchant de la date de péremption':
                notification.title = 'Médicament approchant de la date de péremption'
                notification.message = f"Le médicament {designation} approche de la date de péremption."
                notification.save()
        else:
            notification = Notification(
                user=user,
                medicament_lien_id=medicament_id,
                title='Médicament approchant de la date de péremption',
                message=f"Le médicament {designation} approche de la date de péremption.",
                url='/medicament/' + str(medicament_id)
            )
            notification.save()


            ##3

    # Récupérer toutes les notifications non lues de l'utilisateur
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-timestamp')

    data = [
        {
            'title': notification.title,
            'message': notification.message,
            'url': notification.url,
        }
        for notification in notifications
    ]

    return JsonResponse(data, safe=False)




