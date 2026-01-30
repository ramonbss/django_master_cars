from django.contrib import admin

# Register your models here.
from .models import Car, Brand, CarInventory

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'price')
    search_fields = ('model', 'brand')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CarInventoryAdmin(admin.ModelAdmin):
    list_display = ('cars_count', 'cars_total_value', 'created_at')

admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(CarInventory, CarInventoryAdmin)