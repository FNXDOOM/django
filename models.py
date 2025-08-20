from django.db import models

# Create your models here.

# alerts/models.py

class Alert(models.Model):
    VIOLATION_CHOICES = [
        ('NO_HELMET', 'No Helmet Detected'),
        ('NO_VEST', 'No Safety Vest Detected'),
        
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    violation_type = models.CharField(max_length=50, choices=VIOLATION_CHOICES)
    camera_id = models.CharField(max_length=100, blank=True, null=True)
    snapshot = models.ImageField(upload_to='snapshots/') # Saves images to a 'media/snapshots/' folder

    def __str__(self):
        return f"{self.get_violation_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"