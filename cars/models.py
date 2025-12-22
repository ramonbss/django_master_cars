from django.db import models




class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='cars', null=True, blank=True)
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='cars', blank=True, null=True)

    def __str__(self):
        return f"{self.model} ({self.pk})"