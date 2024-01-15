from django.db import models

# Create your models here.
class fournisseur(models.Model):
   nom = models.CharField(max_length=100)
   tel = models.IntegerField()
   adress= models.TextField()
   qualite=models.CharField(max_length=100,default='parfite')


   def __str__(self):
        return self.nom
   