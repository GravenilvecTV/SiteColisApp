from django.http import HttpResponse
from django.shortcuts import render

from .forms import RegisterParcelForm
from .models import Parcel

# Create your views here.
def home_page(request):
    nb_colis = len(Parcel.objects.all())
    nom_entrepot = "GravenEntrepot"
    context = {
        'nb_colis': nb_colis, 
        'nom_entrepot': nom_entrepot
    }

    return render(request, 'index.html', context=context)

def tracking_page(request):
    parcel = None
    error = None

    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        
        try:
            parcel = Parcel.objects.get(tracking_number=tracking_number)
        except Parcel.DoesNotExist:
            error = "Aucun colis n'existe avec suivi"
        
    return render(request, "tracking.html", { "parcel": parcel, "error": error })

def parcels_page(request):
    return render(request, "parcels.html", context={'colis': Parcel.objects.all()})

def add_parcel_page(request):

    if request.method == 'POST':
        form = RegisterParcelForm(request.POST)
        if form.is_valid():
            form.save() # insertion dans la base
            return HttpResponse("Enregistrement ok")
    else:
        form = RegisterParcelForm()
        return render(request, "add_parcel.html", context={'form': form})