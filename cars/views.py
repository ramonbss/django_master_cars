from django.shortcuts import render, redirect
from django.conf import settings
from .models import Car
from cars.forms import CarFormModel

# Create your views here.
def cars(request):
    cars_list = Car.objects.all()
    search = request.GET.get('search')
    if search:
        cars_list = cars_list.filter(model__icontains=search)
    
    # Enrich each car with safe photo URL (presentation logic)
    for car in cars_list:
        car.photo_url = _get_car_photo_url(car)
    
    context = {
        'cars': cars_list
    }
    return render(request, 'cars.html', context)


def _get_car_photo_url(car):
    """
    Helper function to get the photo URL with fallback to placeholder.
    Keeps presentation logic out of the model layer.
    """
    if car.photo and hasattr(car.photo, 'url'):
        try:
            return car.photo.url
        except ValueError:
            # Photo field exists but no file is associated
            pass
    
    # Fallback to placeholder - uses settings for flexibility
    return f'{settings.MEDIA_URL}cars/car_placeholder.webp'


def new_car(request):
    if request.method == 'POST':
        new_car_form = CarFormModel(request.POST, request.FILES)
        print(new_car_form.data)
        if new_car_form.is_valid():
           new_car_form.save()
           return redirect('cars_list')
    else:
        new_car_form = CarFormModel()
    return render(request, 'new_car.html', context={'new_car_form': new_car_form})