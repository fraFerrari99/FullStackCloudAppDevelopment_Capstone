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


class CarDealer:
    def __init__(self, address, city, full_name, id, 
                lat, long, short_name, st, state, zip):
                self.address = address
                self.city = city
                self.full_name = full_name
                self.id = id
                self.lat = lat
                self.long = long
                self.short_name = short_name
                self.st = st
                self.state = state
                self.zip = zip
    
    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview():
    def __init__(self, dealership, car_make, name, 
                purchase, purchase_date, review, 
                car_year, car_model, another, sentiment, id):
        
        self.dealership=dealership
        self.car_make=car_make
        self.name=name
        self.purchase=purchase
        self.purchase_date=purchase_date
        self.review=review
        self.car_year=car_year
        self.car_model=car_model
        self.another=another
        self.sentiment=sentiment
        self.id=id

    def __str__(self):
        return "Name: " + self.name +", Review: " + self.review