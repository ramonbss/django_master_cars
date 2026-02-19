from celery import shared_task
from cars.models import Car, CarInventory
from django.db.models import Sum


@shared_task
def update_car_inventory():
    cars_count = Car.objects.count()
    cars_total_value = (
        Car.objects.aggregate(total_value=Sum("price"))["total_value"] or 0
    )
    CarInventory.objects.create(
        cars_count=cars_count,
        cars_total_value=cars_total_value,
    )
