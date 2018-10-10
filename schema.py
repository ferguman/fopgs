import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from graphql_server.models import Device, DeviceType, EnvironmentAttribute, EnvironmentObservation, EnvironmentSubject 
from graphql_server.models import EnvironmentSubjectLocation, Location, Organization, Participant, Person
from graphql_server.models import ScalarEnvironmentObservation

class DeviceObj(DjangoObjectType):
    class Meta:
        model = Device

class DeviceTypeObj(DjangoObjectType):
    class Meta:
        model = DeviceType

class EnvironmentAttributeObj(DjangoObjectType):
    class Meta:
        model = EnvironmentAttribute 

class EnvironmentObservationObj(DjangoObjectType):
    class Meta:
        model = EnvironmentObservation 

class EnvironmentSubjectObj(DjangoObjectType):
    class Meta:
        model = EnvironmentSubject 

class EnvironmentSubjectLocationObj(DjangoObjectType):
    class Meta:
        model = EnvironmentSubjectLocation 

class LocationObj(DjangoObjectType):
    class Meta:
        model = Location

class OrganizationObj(DjangoObjectType):
    class Meta:
        model = Organization

class ParticipantObj(DjangoObjectType):
    class Meta:
        model = Participant

class PersonObj(DjangoObjectType):
    class Meta:
        model = Person

class ScalarEnvironmentObservationObj(DjangoObjectType):
    class Meta:
        model = ScalarEnvironmentObservation 

class Query(object):

    # ######## Device #########
    devices = graphene.List(DeviceObj, device_type=graphene.String())

    def resolve_devices(self, info, device_type=None, **kwargs):
        if device_type:
            filter = (
                Q(device_type__local_name__icontains=device_type)
            )
            return Device.objects.filter(filter) 

        return Device.objects.all()

    # ######## DeviceType #########
    device_types = graphene.List(DeviceTypeObj)

    def resolve_device_types(self, info, **kwargs):
        return DeviceType.objects.all()

    # ######## Environment Attribute #########
    environment_attributes = graphene.List(EnvironmentAttributeObj)
    
    def resolve_environment_attributes(self, info, **kwargs):
        return EnvironmentAttribute.objects.all()

    # ######## EnvironmentObservation#########
    environment_observations = graphene.List(EnvironmentObservationObj, attribute_name=graphene.String(),
                                             device_name=graphene.String(), first=graphene.Int())
    
    def resolve_environment_observations(self, info, first=None, device_name=None, attribute_name=None, **kwargs):
        return EnvironmentObservation.objects.order_by()[:50]

    # ######## EnvironmentSubject #########
    environment_subjects = graphene.List(EnvironmentSubjectObj)
    
    def resolve_environment_subjects(self, info, **kwargs):
        return EnvironmentSubject.objects.all()

    # ######## EnvironmentSubjectLocation########
    environment_subject_locations = graphene.List(EnvironmentSubjectLocationObj)
    
    def resolve_environment_subject_locations(self, info, **kwargs):
        return EnvironmentSubjectLocation.objects.all()

    # ######## Location #########
    locations = graphene.List(LocationObj)

    def resolve_locations(self, info, **kwargs):
        return Location.objects.all()

    # ######## Organization #########
    organizations = graphene.List(OrganizationObj, search=graphene.String())

    def resolve_organizations(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(local_name__icontains=search)
            )
            return Organization.objects.filter(filter)

        return Organization.objects.all() 

    # ######## Participant #########
    participants = graphene.List(ParticipantObj, device_type_name=graphene.String())

    def resolve_participants(self, info, device_type_name=None, **kwargs):

        if device_type_name:
            filter = (Q(device__device_type__local_name__icontains=device_type_name))
            return Participant.objects.filter(filter)

        return Participant.objects.all()

    # ######## Person #########
    persons = graphene.List(PersonObj)

    def resolve_persons(self, info, **kwargs):
        return Person.objects.all()

    # ######## ScalarEnvironmentObservation #########
    scalar_environment_observations = graphene.List(ScalarEnvironmentObservationObj, device_guid=graphene.UUID(),  
                                                    attribute_name=graphene.String())

    # environment_observations = graphene.List(EnvironmentObservationObj, attribute_name=graphene.String(),
    #                                         device_name=graphene.String(), first=graphene.Int())
    
    """
    if device_name:
        filter = (Q(
    if first:
        return EnvironmentObservation.objects.all()[:first]
    """

    def resolve_scalar_environment_observations(self, info, device_guid=None, attribute_name=None, **kwargs):

        q = None

        if attribute_name:
            q = ScalarEnvironmentObservation.objects.filter(
                environment_observation__environment_attribute__name__icontains = attribute_name)

        if device_guid:
            if q:
                q = q.filter(environment_observation__participant__guid = device_guid)
            else:
                q = ScalarEnvironmentObservation.objects.filter( 
                    environment_observation__participant__guid = device_guid)


        return q.order_by('-utc_timestamp')[:10]

        #return ScalarEnvironmentObservation.objects.all()[:10]
