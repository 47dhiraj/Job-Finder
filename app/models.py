from django.db import models
from django.core.validators import RegexValidator



class Company(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    address = models.CharField(max_length=120, null=True, blank=True, db_index=True)
    phone_regex = RegexValidator(regex=r'(?:\+977[- ])?9\d{1}-?\d{8}(?!\d)', message="Valid phone no. format: '+977 9845454545' or '9845454545'")
    phone = models.CharField(validators=[phone_regex], max_length=16, null=True, blank=True)



class Job(models.Model):
    JOB_LOCATIONS = (
        ('Onsite','Onsite'),
        ('Remote','Remote'),
        ('Freelance','Freelance'),
        ('Hybrid', 'Hybrid'),
    )

    JOB_TYPES = (
        ('Fulltime','Fulltime'),
        ('Parttime','Parttime'),
    )

    JOB_ROLES = (
        ('Project-Manager','Project-Manager'),
        ('Team-Lead','Team-Lead'),
        ('Developer','Developer'),
        ('Designer','Designer'),
        ('Quality-Assurance','Quality-Assurance'),
    )

    JOB_SCHEDULES = (
        ('10:00 AM - 05:00 PM','10:00 AM - 05:00 PM'),
        ('11:00 AM - 05:00 PM','11:00 AM - 05:00 PM'),
        ('07:00 AM - 03:00 PM','07:00 AM - 03:00 PM'),
        ('08:00 PM - 05:00 AM','08:00 PM - 05:00 AM'),
    )


    title = models.CharField(max_length=120, unique=True, db_index=True)
    location = models.CharField(max_length=120, choices=JOB_LOCATIONS, default= JOB_LOCATIONS[0][0], db_index=True)
    type = models.CharField(max_length=25, choices=JOB_TYPES, default= JOB_TYPES[0][0], db_index=True)
    role = models.CharField(max_length=25, choices=JOB_ROLES, default= JOB_ROLES[2][0], db_index=True)
    schedule = models.CharField(max_length=22, choices=JOB_SCHEDULES, default= JOB_SCHEDULES[0][0])
    vaccancy = models.IntegerField(default=1)
    min_salary = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')

