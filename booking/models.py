from django.db import models

from django.core.exceptions import ValidationError
import uuid

# Create your models here.



class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Chambre(models.Model):
    numero = models.IntegerField(unique=True)
    type = models.CharField(max_length=20, choices=[('simple', 'Simple'), ('double', 'Double'), ('suite', 'Suite')])
    prix_par_nuit = models.FloatField()
    statut = models.BooleanField(default=True)  # True = Disponible, False = Réservée

    def __str__(self):
        return f"Chambre {self.numero} ({self.type})"



class Reservation(models.Model):
    numero_reservation = models.CharField(max_length=10, unique=True, editable=False)
    nom_client = models.CharField(max_length=100)  # Le client entre son nom directement
    chambre = models.ForeignKey('Chambre', on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix_total = models.FloatField(default=0.0)  # Calcul du prix total avec taxes

    def save(self, *args, **kwargs):
        self.clean()  # Appelle la validation avant de sauvegarder
        if not self.numero_reservation:
            self.numero_reservation = str(uuid.uuid4())[:8].upper()
        self.prix_total = self.calculer_prix_total()
        super().save(*args, **kwargs)

    def clean(self):
        # Vérifie les conflits de réservation
        conflits = Reservation.objects.filter(
            chambre=self.chambre,
            date_debut__lt=self.date_fin,  # La réservation commence avant la fin de l'autre
            date_fin__gt=self.date_debut   # La réservation se termine après le début de l'autre
        )
        if conflits.exists():
            raise ValidationError("Cette chambre est déjà réservée pour cette période.")

    def calculer_prix_total(self):
        nombre_nuits = (self.date_fin - self.date_debut).days
        if nombre_nuits < 0:
            nombre_nuits = 0
        prix_sans_taxes = nombre_nuits * self.chambre.prix_par_nuit
        tps = 0.05 * prix_sans_taxes
        tvq = 0.09975 * prix_sans_taxes
        return round(prix_sans_taxes + tps + tvq, 2)

    def __str__(self):
        return f"Réservation {self.numero_reservation} pour {self.nom_client}"

    
    
class Photo(models.Model):
    chambre = models.ForeignKey(Chambre, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chambres/photos/')  # Chemin d'enregistrement des images
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo de la chambre {self.chambre.numero}"
