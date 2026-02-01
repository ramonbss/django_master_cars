from django.db.models.signals import pre_save,post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from cars.models import Car, CarInventory


@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = "Bio gerada automaticamente"

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    update_car_inventory()


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    update_car_inventory()


def update_car_inventory():
    cars_count = Car.objects.count()
    cars_total_value = (
        Car.objects.aggregate(total_value=Sum("price"))["total_value"] or 0
    )
    CarInventory.objects.create(
        cars_count=cars_count,
        cars_total_value=cars_total_value,
    )
