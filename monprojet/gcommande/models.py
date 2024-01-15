from datetime import date
from django.db import models
from gfournisseur.models import fournisseur
from gststock.models import medicament


class gcommandes(models.Model):
    fournisseur = models.ForeignKey(fournisseur, on_delete=models.CASCADE, null=True)
  
    adresse_livraison = models.TextField()
    date_commande =models.DateField(default= date.today)
    imprimee = models.BooleanField(default=False)
    annulee = models.BooleanField(default=False)


    def __str__(self):
        return f"Commande #{self.id}"


class MedicamentsCommande(models.Model):
    commande = models.ForeignKey(gcommandes, on_delete=models.CASCADE,null=True)
    medicament = models.ForeignKey(medicament, on_delete=models.CASCADE,null=True)
    quantite_demandee = models.IntegerField()
    description = models.TextField()
    D = models.FloatField(default=0.0)  # Demande annuelle prévue
    S = models.FloatField(default=0.0)  # Coût unitaire de possession de stock
    C = models.FloatField(default=0.0)  # Coût de commande


    def __str__(self):
        return f"MedicamentCommande #{self.id}"