import hashlib,os,requests
from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets,permissions,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from .models import *
from .serializers import *
from tcc_common.events import publish
class CourseViewSet(viewsets.ModelViewSet): queryset=Course.objects.all(); serializer_class=CourseSerializer
class ProfessorViewSet(viewsets.ModelViewSet): queryset=Professor.objects.all(); serializer_class=ProfessorSerializer
class StudentViewSet(viewsets.ModelViewSet): queryset=Student.objects.all(); serializer_class=StudentSerializer
class DocumentViewSet(viewsets.ModelViewSet):
    queryset=ComplementaryDocument.objects.all().order_by("-uploaded_at")
    serializer_class=DocumentSerializer
    parser_classes=[MultiPartParser,FormParser]

class MonographViewSet(viewsets.ModelViewSet):
 queryset=Monograph.objects.all().order_by("-created_at"); serializer_class=MonographSerializer
 def create(self,request,*a,**kw):
  f=request.FILES.get("file")
  if not f or f.content_type!="application/pdf" or not f.name.lower().endswith(".pdf"): return Response({"detail":"Somente PDF."},status=400)
  if f.size>50*1024*1024: return Response({"detail":"Máximo 50 MB."},status=400)
  h=hashlib.sha256();
  for c in f.chunks(): h.update(c)
  if Monograph.objects.filter(sha256=h.hexdigest()).exists(): return Response({"detail":"Arquivo duplicado.","sha256":h.hexdigest()},status=409)
  f.seek(0); s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); obj=s.save(sha256=h.hexdigest())
  AuditLog.objects.create(user_id=request.user.id,action="upload",monograph_id=obj.id,ip_address=request.META.get("REMOTE_ADDR"))
  cache.set(f"upload_em_andamento:{obj.id}",1,300)
  publish("monograph.submitted",{"id":str(obj.id),"title":obj.title,"file":obj.file.name,"student_id":str(obj.student_id),"advisor_id":str(obj.advisor_id),"course_id":str(obj.course_id)})
  return Response(self.get_serializer(obj).data,status=201)
 @action(detail=True,methods=["post"])
 def approve(self,request,pk=None):
  obj=self.get_object()
  if str(request.user.id)!=str(obj.advisor_id) and request.user.role not in ["admin","coordinator"]: return Response({"detail":"Somente o orientador pode aprovar."},status=403)
  obj.advisor_approved_at=timezone.now(); obj.status=Monograph.Status.REVIEW; obj.save(update_fields=["advisor_approved_at","status","updated_at"])
  AuditLog.objects.create(user_id=request.user.id,action="advisor_approval",monograph_id=obj.id,ip_address=request.META.get("REMOTE_ADDR"))
  publish("monograph.advisor_approved",{"id":str(obj.id),"title":obj.title,"advisor_id":str(obj.advisor_id)})
  return Response(self.get_serializer(obj).data)
 @action(detail=True,methods=["post"])
 def submit(self,request,pk=None):
  obj=self.get_object()
  if not obj.advisor_approved_at: return Response({"detail":"A aprovação do orientador é obrigatória antes da banca."},status=409)
  obj.status=Monograph.Status.REVIEW; obj.submitted_at=obj.submitted_at or timezone.now(); obj.save()
  publish("monograph.ready_for_defense",{"id":str(obj.id),"title":obj.title})
  return Response(self.get_serializer(obj).data)
 @action(detail=True,methods=["post"])
 def revoke_approval(self,request,pk=None):
  obj=self.get_object();
  if request.user.role not in ["admin","coordinator"]: return Response(status=403)
  obj.advisor_approved_at=None; obj.status=Monograph.Status.DRAFT; obj.save(); return Response(self.get_serializer(obj).data)
