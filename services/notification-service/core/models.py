from django.db import models
class Notification(models.Model): event_type=models.CharField(max_length=100); recipient=models.CharField(max_length=255); subject=models.CharField(max_length=255); message=models.TextField(); sent=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
