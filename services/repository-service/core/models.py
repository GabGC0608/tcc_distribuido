import uuid
from django.db import models
class RepositoryMonograph(models.Model):
 id=models.UUIDField(primary_key=True); title=models.CharField(max_length=300); abstract=models.TextField(blank=True); keywords=models.JSONField(default=list); author=models.CharField(max_length=200); advisor=models.CharField(max_length=200); course=models.CharField(max_length=200); defense_year=models.PositiveIntegerField(null=True); file_path=models.CharField(max_length=500); sha256=models.CharField(max_length=64); published_at=models.DateTimeField(); extracted_text=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
