from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car
from cars.forms import CarFormModel


class CarListView(ListView):
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(model__icontains=search)

        return queryset


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarFormModel
    template_name = "new_car.html"
    success_url = reverse_lazy("cars_list")
    context_object_name = "new_car_form"
    login_url = reverse_lazy("login")


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarFormModel
    template_name = "car_update.html"
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse_lazy("car_detail", kwargs={"pk": self.object.pk})


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = "car_delete.html"
    success_url = reverse_lazy("cars_list")
    login_url = reverse_lazy("login")
