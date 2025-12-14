from django.contrib import admin

# Register your models here.
from .models import Car

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'price')
    search_fields = ('model', 'brand')

admin.site.register(Car, CarAdmin)


