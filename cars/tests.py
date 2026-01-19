from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Car, Brand

class CarViewsTest(TestCase):

    def setUp(self):
        # Create a sample brand for testing
        self.brand = Brand.objects.create(name='Test Brand')
        # Create a sample car for testing
        self.car = Car.objects.create(
            model='Test Car',
            brand=self.brand,
            factory_year=2020,
            model_year=2021,
            plate='ABC1234',
            price=50000.0
        )

    def test_cars_view(self):
        response = self.client.get(reverse('cars_list'))  # Adjust the URL name as necessary
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars.html')
        self.assertContains(response, 'Test Car')  # Check if the car is in the response

    def test_new_car_view_get(self):
        response = self.client.get(reverse('new_car'))  # Adjust the URL name as necessary
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_car.html')

    def test_new_car_view_post(self):
        # Create a simple uploaded file for photo
        photo = SimpleUploadedFile("test_photo.jpg", b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9', content_type="image/jpeg")
        response = self.client.post(reverse('new_car'), {
            'model': 'New Car',
            'brand': self.brand.id,
            'factory_year': 2022,
            'model_year': 2023,
            'plate': 'XYZ5678',
            'price': 60000.0,
            'photo': photo,
        })
        
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Car.objects.filter(model='New Car').exists())

    def test_cars_view_search(self):
        response = self.client.get(reverse('cars_list') + '?search=Test')
        self.assertContains(response, 'Test Car')
        self.assertNotContains(response, 'Nonexistent Car')
