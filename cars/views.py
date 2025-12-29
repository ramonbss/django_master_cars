from django.shortcuts import render
from .models import Car

# Create your views here.
def cars(request):
    cars = Car.objects.all()
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context)
