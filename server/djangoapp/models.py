from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=300,null=False)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    TYPES = (
    ("SUV", "Suv"),
    ("WAGON", "Wagon"),
    ("SEDAN", "Sedan"),
    ("COUPE","Coupe"),
    ("MINIVAN","Minivan"),
    ("PICKUP","Pickup")
  )
    car_make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    dealer_id = models.IntegerField(null=False)
    types = models.CharField(max_length=10,choices=TYPES)
    year = models.DateField()

    def __str__(self):
        return str(self.car_make) + " " + self.name + ", Year " + str(self.year.year)  

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
