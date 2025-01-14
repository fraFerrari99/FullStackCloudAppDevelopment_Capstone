from django.contrib import admin
from .models import CarMake,CarModel
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
    
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make','name','types')
    list_filter = ('car_make','name','types')


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name']
    list_filter = ['name']

# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)