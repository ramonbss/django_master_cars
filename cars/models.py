from django.db import models

from app import settings


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="cars", null=True, blank=True
    )
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    plate = models.CharField(max_length=10)
    price = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to="cars", blank=True, null=True)

    @property
    def photo_url(self):
        """
        Returns the URL for the car's photo or a placeholder

        This is a computed property that:
        1. Returns actual photo URL if exists
        2. Returns placeholder URL if photo is empty
        3. Can be accessed like: car.photo_url (no parentheses needed)

        Returns:
            str: URL to photo or placeholder image
        """
        if self.photo:  # Django's ImageField evaluates to False when empty
            try:
                return self.photo.url
            except (ValueError, AttributeError):
                # Edge case: photo field corrupted or file deleted from disk
                pass

        # Return placeholder from static files
        return f"{settings.STATIC_URL}images/car_placeholder.webp"

    @property
    def has_photo(self):
        """
        Check if car has a custom photo
        Useful for conditional rendering in templates
        """
        return bool(self.photo)

    def __str__(self):
        return f"{self.model} ({self.pk})"


class CarInventory(models.Model):
    cars_count = models.IntegerField()
    cars_total_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cars_count} - {self.cars_total_value}"
