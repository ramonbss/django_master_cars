from django import forms
from cars.models import Brand

class CarForm(forms.Form):
    model = forms.CharField(max_length=200)
    brand = forms.ModelChoiceField(Brand.objects.all())
    factory_year = forms.IntegerField()
    model_year = forms.IntegerField()
    plate = forms.CharField(max_length=10)
    price = forms.FloatField()
    photo = forms.ImageField()

    def save(self):
        data = self.cleaned_data
        from cars.models import Car # Imported here to avoid circular imports
        car = Car(
            model=data['model'],
            brand=data['brand'],
            factory_year=data['factory_year'],
            model_year=data['model_year'],
            plate=data['plate'],
            price=data['price'],
            photo=data['photo']
        )
        car.save()
        return car
    