from django.db import models
from django.db.models import Q

class Device(models.Model):

    participant = models.OneToOneField('Participant', primary_key=True, db_column='guid', 
                                       on_delete=models.CASCADE, related_name='device')
    parent_device = models.ForeignKey('self', on_delete=models.CASCADE, db_column='parent_guid', 
                                      null=True, related_name='sub_devices')
    device_type = models.ForeignKey('DeviceType_m', models.DO_NOTHING)
    local_name = models.CharField(max_length=75)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceType_m(models.Model):

    local_name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'device_type'


class EnvironmentAttribute(models.Model):

    name = models.CharField(unique=True, max_length=75)

    class Meta:
        managed = False
        db_table = 'environment_attribute'


class EnvironmentObservation(models.Model):

    participant = models.ForeignKey('Participant', models.DO_NOTHING, db_column='participant_guid',
                                    related_name='environment_observations')
    environment_subject_location = models.ForeignKey('EnvironmentSubjectLocation', 
                                                      models.DO_NOTHING, db_column='environment_subject_location_guid', 
                                                      related_name='environment_observations')
    environment_attribute = models.ForeignKey(EnvironmentAttribute, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'environment_observation'

class EnvironmentSubject(models.Model): 

    name = models.CharField(unique=True, max_length=75) 

    class Meta:
        managed = False
        db_table = 'environment_subject'


class EnvironmentSubjectLocation(models.Model): 

    guid = models.UUIDField(primary_key=True) 
    environment_subject = models.ForeignKey(EnvironmentSubject, models.DO_NOTHING) 
    location_guid = models.ForeignKey('Location', models.DO_NOTHING, db_column='location_guid') 
 
    class Meta: 
        managed = False 
        db_table = 'environment_subject_location' 


class Location(models.Model):

    guid = models.UUIDField(primary_key=True)
    #parent_id = models.UUIDField(blank=True, null=True)
    parent_location = models.ForeignKey('self', on_delete=models.CASCADE, null=True, db_column='parent_id', related_name='sub_location')
    local_name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'location'


class Organization(models.Model):

    guid = models.UUIDField(primary_key=True)
    parent_org = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='sub_organization')
    local_name = models.CharField(max_length=75, db_column='local_name')

    class Meta:
        managed = False
        db_table = 'organization'


class Participant(models.Model): 

    guid = models.UUIDField(primary_key=True) 
    organization = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization_guid', blank=True, null=True) 
 
    class Meta: 
        managed = False 
        db_table = 'participant' 


class Person(models.Model):

    #participant = models.OneToOneField(Participant, primary_key=True, db_column='guid', parent_link=True, 
    #                                   on_delete=models.CASCADE)
    participant = models.OneToOneField(Participant, primary_key=True, db_column='guid',  
                                       on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=75)

    class Meta:
        managed = True
        db_table = 'person'

class ScalarEnvironmentObservation(models.Model): 

    environment_observation = models.OneToOneField(EnvironmentObservation, primary_key=True, 
                                                   db_column='environment_observation_id',
                                                   on_delete=models.CASCADE) 
                                                   # parent_link=True, on_delete=models.CASCADE) 
    measurement_value = models.FloatField() 
    units = models.CharField(max_length=75) 
    utc_timestamp = models.DateTimeField() 
 
    class Meta: 
        managed = False 
        db_table = 'scalar_environment_observation'
