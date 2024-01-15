from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
from .forms import userForm,ProfilForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def is_gerant(user):
    return user.profile.grade == 'gerant'


@login_required
@user_passes_test(is_gerant)

def register(request):
    registered = False
    if request.method == "POST":
        user_form = userForm(data=request.POST)
        profil_form = ProfilForm(data=request.POST)
        if user_form.is_valid() and profil_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profil_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return HttpResponseRedirect('agents')

        else:
            print(user_form.errors,profil_form.errors)
    else:
        user_form = userForm()
        profil_form = ProfilForm()
    content ={
        'registred':registered,
        'form1':user_form,
        'form2':profil_form,
    }
    return render(request, 'utilisateur/register.html',content)
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        grade = request.POST.get('grade')

        user = authenticate(username=username, password=password, grade=grade)
        if user:
            if user.is_active:
                login(request, user)

                # Récupérer le profil de l'utilisateur
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    profile = None

                # Rediriger l'utilisateur vers la page correspondante en fonction de son grade
                if profile:
                    if profile.grade == 'gerant':
                        return redirect('menu')
                    elif profile.grade == 'employe':
                        return redirect('stock')
                else:
                    return HttpResponse("Le profil de l'utilisateur n'a pas été trouvé.")
            else:
                return HttpResponse("L'utilisateur est désactivé.")
        else:
             error_message = "Le nom d'utilisateur et/ou le mot de passe sont incorrects."
             return render(request, 'utilisateur/login.html', {'error_message': error_message})

    else:
        return render(request,'utilisateur/login.html')
      
@login_required
def user_logout(request):
    logout(request)
    #
    return HttpResponseRedirect('login')

@login_required

@user_passes_test(is_gerant)

def agents(request):

    if 'q' in request.GET:
       q = request.GET['q']
       profiles= Profile.objects.filter(user__first_name__icontains=q)
       context = {
        'profiles': profiles,
    }
    else:
      profiles = Profile.objects.all()
    
      context = {'profiles': profiles, }
    return render(request, 'utilisateur/agents.html', context)



def editagent(request):
 profiles = Profile.objects.filter(id = id)

 context = {
   'profiles': profiles,
 }

 return redirect(request,'utilisateur/agent.html',context)


def updateagent(request, id):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        adress = request.POST.get('adress')

        # Obtenir l'instance du profil à mettre à jour
        profile = Profile.objects.get(id=id)

        # Mettre à jour les attributs du profil
        profile.user.username = username
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.tel = tel
        profile.user.email = email
        profile.adress = adress

        # Sauvegarder les modifications du profil et de l'utilisateur associé
        profile.user.save()
        profile.save()

        return redirect('agents')

    return redirect('utilisateur/agents.html')





def deleteagents(request,id):
       profiles = Profile.objects.filter(id = id)
       profiles.delete()
       context = {
      'profiles': profiles,
    }
       return redirect('agents')



