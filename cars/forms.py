from django import forms
from cars.models import Car
from datetime import datetime
    
class CarFormModel(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    def clean_plate(self):
        plate = self.cleaned_data.get('plate')
        if not plate:
            raise forms.ValidationError("Plate field cannot be empty.")
        if len(plate) < 4:
            raise forms.ValidationError("Plate must be at least 4 characters long.")
        return plate

    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        self._validate_year(factory_year)
        return factory_year
    
    def clean_model_year(self):
        model_year = self.cleaned_data.get('model_year')
        self._validate_year(model_year)
        return model_year
    
    def _validate_year(self, year):
        if year and (year < 1886 or year > datetime.now().year + 1):
            raise forms.ValidationError(f"Year must be between 1886 and {datetime.now().year + 1}.")
        return year
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    