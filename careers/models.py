import uuid

from django.db import models

# Create your models here.
from companies.models import Company

JOB_SCHEDULE_CHOICES = (
    ("REMOTE", "REMOTE"),
    ("CONTRACT", "CONTRACT"),
    ("FULL-TIME", "FULL-TIME"),
)


class JobSchedule(models.Model):
    """
    this contains the categories of jobs which is either contract,fulltime or remote
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    job_schedule = models.CharField(choices=JOB_SCHEDULE_CHOICES, max_length=250, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Applicant(models.Model):
    """
    this contains list of user who applied to a job
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    first_name = models.CharField(max_length=250)
    email = models.EmailField()
    image = models.ImageField(upload_to="applicants")
    last_name = models.CharField(max_length=250)
    nationality = models.CharField(max_length=250)
    country_of_residence = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=50)
    home_address = models.CharField(max_length=250)
    experience = models.JSONField(blank=True, null=True)
    education = models.JSONField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to="resumes")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


JOB_TYPE_CHOICES = (
    ("DEVELOPER", "DEVELOPER"),
    ("ANIMATION", "ANIMATION"),
    ("ANIMATION", "ANIMATION"),
    ("DESIGN", "DESIGN"),
)


class Job(models.Model):
    """the contains list of jobs that are available under a company """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_type = models.CharField(choices=JOB_TYPE_CHOICES, max_length=250)
    job_schedules = models.ManyToManyField(JobSchedule, blank=True)
    applicants = models.ManyToManyField(Applicant, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def applicant_counts(self):
        return self.applicants.count()