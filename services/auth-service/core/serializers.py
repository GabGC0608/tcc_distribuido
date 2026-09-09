from rest_framework import serializers
from .models import User,AuditLog
class UserSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,min_length=10)
 class Meta: model=User; fields=["id","email","first_name","last_name","role","matricula","course_id","password"]
 def create(self,v): return User.objects.create_user(username=v["email"],**v)
class AuditSerializer(serializers.ModelSerializer):
 class Meta: model=AuditLog; fields="__all__"
