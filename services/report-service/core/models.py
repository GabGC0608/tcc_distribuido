from django.db import models
class Metric(models.Model): key=models.CharField(max_length=100); value=models.JSONField(default=dict); updated_at=models.DateTimeField(auto_now=True)
