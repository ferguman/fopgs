from django.contrib import admin
from .models import Device, DeviceType, EnvironmentAttribute, EnvironmentSubject, Location,  Organization, Participant, Person
from .models import PhenotypeImage, PhenotypeObservation, PlantGroup, ScalarEnvironmentObservation

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(EnvironmentAttribute)
admin.site.register(EnvironmentSubject)
admin.site.register(Location)
admin.site.register(Organization)
admin.site.register(Participant)
admin.site.register(Person)
admin.site.register(PhenotypeImage)
admin.site.register(PhenotypeObservation)
admin.site.register(PlantGroup)
admin.site.register(ScalarEnvironmentObservation)
