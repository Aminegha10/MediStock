from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test

from .models import fournisseur
# Create your views here.

def is_gerant(user):
    return user.profile.grade == 'gerant'

@login_required
@user_passes_test(is_gerant)
def listefournisseurs(request):
  
    if 'q' in request.GET:
       q = request.GET['q']
       frn = fournisseur.objects.filter(nom__icontains=q)
       context = {
        'frn':frn,
    }
    else:
        frn = fournisseur.objects.all()       
    context = {'frn': frn}
    return render(request, 'gfournisseur/fournisseurs.html', context)

def addfournisseur(request):
    if request.method == "POST" :
      nom = request.POST.get('nom')
      tel = request.POST.get('tel')
      adress= request.POST.get('adress')
      qualite = request.POST['qualite']
      
      data = fournisseur (
       nom=nom,
       tel=tel,
      adress=adress,
      qualite=qualite
     )
      data.save()
      
      return redirect('fournisseurs')
    return render(request,'gfournisseur/fournisseurs.html')


def editfournisseur(request):
 frn = fournisseur.objects.all()
 context = {
    'frn':frn,
 }

 return redirect(request,'gfournisseur/fournisseurs.html',context)

def updatefournisseur(request,id):
 if request.method == "POST" :
        nom = request.POST.get('nom')
        tel= request.POST.get('tel')
        email= request.POST.get('email')
        adress = request.POST.get('adress')
        qualite =request.POST.get('qualite')
        data = fournisseur (
        id = id,
       
         nom=nom,
        tel=tel,
        adress=adress,
        qualite=qualite,
       )
        data.save()
        return redirect('fournisseurs')
 return redirect(request,'gfournisseur/fournisseurs.html')

def deletefournisseur(request,id):
       frn = fournisseur.objects.filter(id = id)
       frn.delete()
       context = {
       'frn':frn,
    }
       return redirect('fournisseurs')



