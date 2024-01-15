from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class medicament(models.Model):

    CodeBarre = models.DecimalField(max_digits=20,decimal_places=5)
    designation = models.CharField(max_length=50)
    categorie = models.CharField(max_length=100)
    forme = models.CharField(max_length=50,null=True,blank=True)
    DCI= models.CharField(max_length=50,null=True,blank=True)
    qte = models.IntegerField(null=True,blank=True)
    dosage = models.IntegerField(null=True,blank=True)
    prix_vente = models.DecimalField(max_digits=20,decimal_places=7,null=True,blank=True)
    stock_min = models.IntegerField(null=True,blank=True)
    prix_achat =models.DecimalField(max_digits=20,decimal_places=7,null=True,blank=True)
    date_permeotion = models.DateField()
    lieu_med = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.designation
    

    # gstock/models.py

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicament_lien = models.ForeignKey(medicament, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    url = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


