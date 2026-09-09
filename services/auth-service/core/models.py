import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
class User(AbstractUser):
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
 class Roles(models.TextChoices):
  ADMIN="admin","Administrador"; COORD="coordinator","Coordenador"; PROFESSOR="professor","Professor/Orientador"; STUDENT="student","Aluno"; EXTERNAL="external","Externo"
 username=models.CharField(max_length=150,unique=True,blank=True,null=True)
 email=models.EmailField(unique=True)
 role=models.CharField(max_length=20,choices=Roles.choices,default=Roles.STUDENT)
 USERNAME_FIELD="email"
 REQUIRED_FIELDS=[]
 matricula=models.CharField(max_length=50,blank=True)
 course_id=models.UUIDField(null=True,blank=True)
 class Meta: ordering=["last_name","first_name"]
 def __str__(self): return self.email
class AuditLog(models.Model):
 user_id=models.UUIDField(null=True,blank=True); action=models.CharField(max_length=100); resource=models.CharField(max_length=100); resource_id=models.UUIDField(null=True,blank=True); ip_address=models.GenericIPAddressField(null=True,blank=True); metadata=models.JSONField(default=dict); created_at=models.DateTimeField(auto_now_add=True)
