from datetime import date
from django.db import models
from client.models import patients
from gststock.models import medicament


class Facture(models.Model):
    patient = models.ForeignKey(patients, on_delete=models.CASCADE, null=True)
  
    date_facture =models.DateField(default= date.today)
    imprimee = models.BooleanField(default=False)
    annulee = models.BooleanField(default=False)


    def __str__(self):
        return f"Facture #{self.id}"


class MedicamentsFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE,null=True)
    medicament = models.ForeignKey(medicament, on_delete=models.CASCADE,null=True)
    quantite_demandee = models.IntegerField()


    def __str__(self):
        return f"MedicamentFacture #{self.id}"