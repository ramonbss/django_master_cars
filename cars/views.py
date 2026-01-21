from django.shortcuts import render, redirect
from django.conf import settings
from .models import Car
from cars.forms import CarFormModel
from django.views.generic.list import ListView


class CarListView(ListView):
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(model__icontains=search)

        # Enrich each car with safe photo URL (presentation logic)
        for car in queryset:
            car.photo_url = self._get_car_photo_url(car)

        return queryset

    def _get_car_photo_url(self, car):
        """
        Helper function to get the photo URL with fallback to placeholder.
        Keeps presentation logic out of the model layer.
        """
        if car.photo and hasattr(car.photo, "url"):
            try:
                return car.photo.url
            except ValueError:
                # Photo field exists but no file is associated
                pass

        # Fallback to placeholder - uses settings for flexibility
        return f"{settings.MEDIA_URL}cars/car_placeholder.webp"


def new_car(request):
    if request.method == "POST":
        new_car_form = CarFormModel(request.POST, request.FILES)
        print(new_car_form.data)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect("cars_list")
    else:
        new_car_form = CarFormModel()
    return render(request, "new_car.html", context={"new_car_form": new_car_form})
