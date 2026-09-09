import uuid,hashlib,os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
class Course(models.Model): id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); name=models.CharField(max_length=200); code=models.CharField(max_length=30,unique=True); coordinator_id=models.UUIDField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
class Professor(models.Model): id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); name=models.CharField(max_length=200); email=models.EmailField(unique=True); department=models.CharField(max_length=150,blank=True); research_area=models.CharField(max_length=250,blank=True)
class Student(models.Model): id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); name=models.CharField(max_length=200); matricula=models.CharField(max_length=50,unique=True); email=models.EmailField(unique=True); course_id=models.UUIDField(); advisor_id=models.UUIDField(null=True,blank=True)
class Monograph(models.Model):
 class Status(models.TextChoices): DRAFT="draft","Rascunho"; REVIEW="review","Em avaliação"; APPROVED="approved","Aprovada"; REJECTED="rejected","Reprovada"; PUBLISHED="published","Publicada"
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); title=models.CharField(max_length=300); abstract=models.TextField(blank=True); keywords=models.JSONField(default=list); student_id=models.UUIDField(); advisor_id=models.UUIDField(); course_id=models.UUIDField(); student_name=models.CharField(max_length=200,blank=True); advisor_name=models.CharField(max_length=200,blank=True); course_name=models.CharField(max_length=200,blank=True); defense_year=models.PositiveIntegerField(null=True,blank=True); submitted_at=models.DateTimeField(null=True,blank=True); file=models.FileField(upload_to="monographs/%Y/%m/",validators=[FileExtensionValidator(["pdf"])]); sha256=models.CharField(max_length=64,blank=True); status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT); extracted_text=models.TextField(blank=True); advisor_approved_at=models.DateTimeField(null=True,blank=True); published_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 def clean(self):
  if self.file and self.file.size>50*1024*1024: raise ValidationError("Arquivo maior que 50 MB")
 def save(self,*a,**kw):
  if self.file and not self.sha256:
   h=hashlib.sha256(); self.file.seek(0)
   for chunk in self.file.chunks(): h.update(chunk)
   self.sha256=h.hexdigest(); self.file.seek(0)
  self.full_clean(); return super().save(*a,**kw)
class ComplementaryDocument(models.Model):
 monograph_id=models.UUIDField(); type=models.CharField(max_length=80); file=models.FileField(upload_to="documents/%Y/%m/"); uploaded_at=models.DateTimeField(auto_now_add=True)
class AuditLog(models.Model): user_id=models.UUIDField(null=True); action=models.CharField(max_length=100); monograph_id=models.UUIDField(null=True); metadata=models.JSONField(default=dict); ip_address=models.GenericIPAddressField(null=True); created_at=models.DateTimeField(auto_now_add=True)
