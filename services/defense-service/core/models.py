import uuid,secrets
from django.db import models
class Defense(models.Model):
 class Status(models.TextChoices): SCHEDULED="scheduled","Agendada"; HELD="held","Realizada"; CANCELLED="cancelled","Cancelada"
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); monograph_id=models.UUIDField(); date=models.DateTimeField(); location=models.CharField(max_length=300,blank=True); remote_link=models.URLField(blank=True); status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED); created_at=models.DateTimeField(auto_now_add=True)
class Member(models.Model):
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); defense_id=models.UUIDField(); user_id=models.UUIDField(null=True,blank=True); name=models.CharField(max_length=200); email=models.EmailField(); external=models.BooleanField(default=False); token=models.CharField(max_length=128,unique=True,default=lambda:secrets.token_urlsafe(48)); available=models.BooleanField(default=False); confirmed_at=models.DateTimeField(null=True,blank=True)
class Evaluation(models.Model):
 class Recommendation(models.TextChoices): PASS="approved","Aprovado sem ressalvas"; PASS_FIX="approved_with_reservations","Aprovado com ressalvas"; FAIL="rejected","Reprovado"
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); defense_id=models.UUIDField(); member_id=models.UUIDField(); grade=models.DecimalField(max_digits=5,decimal_places=2); opinion=models.TextField(); recommendation=models.CharField(max_length=40,choices=Recommendation.choices); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
