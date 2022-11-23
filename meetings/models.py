from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

meeting_types = (
    ("MANCO", "MANCO"),
    ("Finance", "Finance"),
    ("Project Team Leaders", "Project Team Leaders")
)
statuses = (
    ("Open","Open"),
    ("In Development","In Development"),
    ("Awaiting Invoicing","Awaiting Invoices"),
    ("Closed","Closed"),
)

# Create your models here.
class Staff(AbstractUser):
    names = models.CharField(max_length=100, null=True)
    initials = models.CharField(max_length=5, null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.names


class Meeting(models.Model):
    meeting_type = models.CharField(choices=meeting_types, null=True, max_length=50)
    meeting_number = models.CharField(null=True, max_length=50)
    meeting_date = models.CharField(null=True, max_length=100)
    meeting_time = models.CharField(null=True, max_length=100)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.meeting_number


class MeetingItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, related_name='meeting')
    name = models.CharField(null=True, max_length=100)
    count = models.IntegerField(null=True)
    label = models.CharField(null=True, max_length=100)
    due_date = models.CharField(null=True, max_length=100)
    person_responsible = models.ForeignKey(Staff,on_delete=models.CASCADE, null=True, related_name='person_responsible')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class MeetingItemStatus(models.Model):
    meeting_item = models.ForeignKey(MeetingItem, on_delete=models.CASCADE, null=True, related_name='meeting_item')
    action = models.TextField()
    status = models.CharField(max_length=100, choices=statuses,null=True)
    count = models.IntegerField(null=True)
    label = models.CharField(null=True, max_length=100)
    person_responsible = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, related_name='staff_responsible')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.action
