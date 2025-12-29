from django.shortcuts import render
from django.conf import settings
from .models import Car

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
