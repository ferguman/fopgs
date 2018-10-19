from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import Q

class Device(models.Model):

    participant = models.OneToOneField('Participant', primary_key=True, db_column='guid', 

                                       on_delete=models.CASCADE, related_name='device')
    parent_device = models.ForeignKey('self', on_delete=models.CASCADE, db_column='parent_guid', 
                                      null=True, blank=True, related_name='sub_devices')
    device_type = models.ForeignKey('DeviceType', models.DO_NOTHING)
    local_name = models.CharField(max_length=75)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location_id', blank=True, null=True)
    configuration = JSONField()

    class Meta:
        managed = False
        db_table = 'device'

    def __str__(self):
        return self.local_name

class DeviceType(models.Model):

    local_name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'device_type'

    def __str__(self):
        return self.local_name


class EnvironmentAttribute(models.Model):

    name = models.CharField(unique=True, max_length=75)

    class Meta:
        managed = False
        db_table = 'environment_attribute'

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.local_name


class Organization(models.Model):

    guid = models.UUIDField(primary_key=True)
    parent_org = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_organization')
    local_name = models.CharField(max_length=75, db_column='local_name')

    class Meta:
        managed = False
        db_table = 'organization'

    def __str__(self):
        return self.local_name

class Person(models.Model): 

    participant = models.OneToOneField('Participant', primary_key=True, db_column='guid', 
                                       on_delete=models.CASCADE, related_name='person')

    nick_name = models.CharField(max_length=75, db_column='nick_name')
    django_username = models.CharField(max_length=150, db_column='django_username')

    class Meta:
        managed = False
        db_table = 'person'

    def __str__(self):
        return self.django_username

class Participant(models.Model): 

    guid = models.UUIDField(primary_key=True) 
    organization = models.ForeignKey(Organization, models.CASCADE, 
                                     db_column='organization_guid', blank=True, null=True) 
 
    class Meta: 
        managed = False 
        db_table = 'participant' 


class PhenotypeImage(models.Model):

    phenotype_observation = models.OneToOneField('PhenotypeObservation', primary_key=True, 
                                                 db_column='phenotype_observation_id',
                                                 on_delete=models.CASCADE) 
    s3_reference = models.CharField(max_length=256) 
 
    class Meta: 
        managed = True 
        db_table = 'phenotype_image'

    def __str__(self):
        return str(self.phenotype_observation)

class PhenotypeObservation(models.Model):

    participant = models.ForeignKey('Participant', models.DO_NOTHING, db_column='participant_guid',
                                    related_name='phenotype_observations')
    plant_group = models.ForeignKey('PlantGroup', models.DO_NOTHING, db_column='plant_group_guid',
                                    related_name='phenotype_observations')
    utc_timestamp = models.DateTimeField() 

    class Meta:
        managed = True
        db_table = 'phenotype_observation'

    def __str__(self):
        return str(self.id)

class PlantGroup(models.Model):

    guid = models.UUIDField(primary_key=True, db_column='guid')
    local_name = models.CharField(max_length=75, blank=False, null=False) 

    class Meta:
        managed = True
        db_table = 'plant_group'

    def __str__(self):
        return str(self.local_name)


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
