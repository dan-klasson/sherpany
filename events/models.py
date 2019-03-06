from django.db import models
from accounts.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="attending"
    )
