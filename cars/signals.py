from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from cars.models import Car
from cars.tasks import update_car_inventory


@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = "Bio gerada automaticamente"


@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    update_car_inventory.delay()


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    update_car_inventory.delay()
