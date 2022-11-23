from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

meeting_types = (
    ("MANCO", "MANCO"),
    ("Finance", "Finance"),
    ("Project Team Leaders", "Project Team Leaders")
)


# Create your models here.
class Staff(AbstractUser):
    names = models.CharField(max_length=100, null=True)
    initials = models.CharField(max_length=5, null=True)
    created_on = models.DateTimeField(default=timezone.now)


class Meeting(models.Model):
    meeting_type = models.CharField(choices=meeting_types, null=True, max_length=50)
    meeting_number = models.CharField(null=True, max_length=50)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


class MeetingItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
    name = models.CharField(null=True, max_length=100)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


class MeetingItemStatus(models.Model):
    meeting_item = models.ForeignKey(MeetingItem, on_delete=models.CASCADE, null=True, related_name='meeting_item')
    action = models.TextField()
    person_responsible = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, related_name='staff_responsible')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
