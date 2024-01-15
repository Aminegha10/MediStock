from django.db import models
from gststock.models import medicament

# Create your models here.
class vente(models.Model):
    medicament = models.ForeignKey(medicament, on_delete=models.CASCADE)
    quantite_vendue = models.PositiveIntegerField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_vente = models.DateField(auto_now_add=True)
    heure_vente = models.TimeField(auto_now_add=True)
    prix_rendu = models.DecimalField(max_digits=10, decimal_places=2)
    reste_a_payer = models.DecimalField(max_digits=10, decimal_places=2)


    