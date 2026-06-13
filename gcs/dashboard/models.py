from django.db import models

# Create your models here.
class Articles(models.Model):
    header = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    day = models.IntegerField()          
    timerange = models.CharField(max_length=50)
    event = models.CharField(max_length=255)  
    note = models.TextField(blank=True)

class Notice(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    notified_at = models.DateTimeField(auto_now_add=True)