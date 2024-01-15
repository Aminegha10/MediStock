from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   tel = models.IntegerField()
   adress = models.TextField()
   gerant = 'gerant'
   employe = 'employe'
   type_user = [
      (gerant , 'gerant'),(employe , 'employe')
   ]
   grade = models.CharField(max_length=100, choices=type_user,default=gerant)


   
   def get_password(self):
        return self.user.password
