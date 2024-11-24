from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Reservation, Chambre
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.core.exceptions import ValidationError

#index



def index(request):
    chambres = Chambre.objects.all()  # Récupérer toutes les chambres
    return render(request, 'booking/index.html', {'chambres': chambres}) 
def details_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    return render(request, 'booking/details_chambre.html', {'chambre': chambre})



def rechercher_reservation(request):
    numero = request.GET.get('numero_reservation', None)
    reservation = None
    if numero:
        reservation = Reservation.objects.filter(numero_reservation=numero).first()
    return render(request, 'booking/rechercher_reservation.html', {'reservation': reservation})

#faire une reservation 


def faire_reservation(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.chambre = chambre
                reservation.save()
                return redirect('confirmation_reservation', reservation.numero_reservation)
            except ValidationError as e:
                form.add_error(None, e.message)  # Ajoute l'erreur globale au formulaire
    else:
        form = ReservationForm(initial={'chambre': chambre})

    return render(request, 'booking/faire_reservation.html', {'form': form, 'chambre': chambre})



def confirmation_reservation(request, numero_reservation):
    reservation = get_object_or_404(Reservation, numero_reservation=numero_reservation)
    return render(request, 'booking/confirmation_reservation.html', {'reservation': reservation})

