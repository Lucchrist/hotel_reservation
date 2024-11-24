from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom_client', 'chambre', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'chambre': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        chambre = cleaned_data.get('chambre')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        # Vérifie les conflits avec des réservations existantes
        conflits = Reservation.objects.filter(
            chambre=chambre,
            date_debut__lt=date_fin,
            date_fin__gt=date_debut
        )
        if conflits.exists():
            raise forms.ValidationError("Cette chambre est déjà réservée pour cette période.")
