from django.contrib import admin
from .models import *
admin.site.register([Course,Professor,Student,Monograph,ComplementaryDocument,AuditLog])
