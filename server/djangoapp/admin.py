from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarMakeInline(admin.StackedInline):
    model = Question
    extra = 5

# Register your models here.

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_car' ,'year')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines=[CarModelAdmin]
    list_display = ['name', 'description']




# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)