from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import patients
# Create your views here.
@login_required

def patient(request):
 if 'q' in request.GET:
       q = request.GET['q']
       pat= patients.objects.filter(nom__icontains=q)
       context = {
        'pat':pat,
    }
 else:
       pat = patients.objects.all()
       
 context = {'pat': pat}
 return render(request, 'client/clients.html',context)
def addpatient(request):
    if request.method == "POST" :
      nom = request.POST.get('nom')
      tel = request.POST.get('tel')
      email = request.POST.get('email')
      adress= request.POST.get('adress')
      
      data = patients (
       nom=nom,
       tel=tel,
      email=email,
      adress=adress
     )
      data.save()
      
      return redirect('clients')
    return render(request,'client/clients.html')


def editpatient(request):
 pat= patients.objects.all()
 context = {
    'pat':pat,
 }

 return redirect(request,'client/clients.html',context)

def updatepatient(request,id):
 if request.method == "POST" :
        nom = request.POST.get('nom')
        tel= request.POST.get('tel')
        email= request.POST.get('email')
        adress = request.POST.get('adress')
        data = patients (
        id = id,
       
         nom=nom,
        tel=tel,
      email=email,
        adress=adress)
        data.save()
        return redirect('clients')
 return redirect(request,'client/clients.html')

def deletepatient(request,id):
       pat = patients.objects.filter(id = id)
       pat.delete()
       context = {
       'pat':pat,
    }
       return redirect('clients')



