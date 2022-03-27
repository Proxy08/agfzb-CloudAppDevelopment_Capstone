from turtle import color
from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

# CarMake model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("MERCEDES", "Mercedes"), ("WAGON", "Wagon"), ("LIMOUSINE", "Limousine") 
        )
    name = models.CharField(max_length=30)
    type_car = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField()
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(null=True)
    content = models.TextField()
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type car: " + self.type_car

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    address = models.CharField(null=False, max_length=30)
    full_name = models.CharField(null=False, max_length=30)
    short_name = models.CharField(null=False, max_length=30)
    city = models.CharField(null=False, max_length=30)
    lat =  models.FloatField(default=5.0)
    long =  models.FloatField(default=5.0)
    st = models.CharField(null=False, max_length=30)
    zip = models.CharField(null=False, max_length=30)
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, car_model, car_make, car_year,purchase,  purchase_date,  sentiment, id):
        self.dealership=dealership,
        self.name = name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment #Watson NLU service
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment