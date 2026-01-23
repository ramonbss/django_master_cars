from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from .models import Car
from cars.forms import CarFormModel
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


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


class CarCreateView(CreateView):
    model = Car
    form_class = CarFormModel
    template_name = "new_car.html"
    success_url = reverse_lazy("cars_list")
    context_object_name = "new_car_form"


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context["photo_url"] = self._get_car_photo_url(car)
        return context

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


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarFormModel
    template_name = "car_update.html"

    def get_success_url(self):
        return reverse_lazy("car_detail", kwargs={"pk": self.object.pk})


class CarDeleteView(DeleteView):
    model = Car
    template_name = "car_delete.html"
    success_url = reverse_lazy("cars_list")
