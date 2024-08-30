from django.db import models

# Create your models here.

class VideoQueue(models.Model):
    video_url = models.URLField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('downloading', 'Downloading'), ('completed', 'Completed')])
    video_title = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
