from django.db import models

# Create your models here.
class patients(models.Model):

   nom = models.CharField(max_length=150)
   tel = models.IntegerField()
   email = models.CharField(max_length=150)
   adress= models.TextField()
   def __str__(self):
        return self.nom
   