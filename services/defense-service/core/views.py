import requests
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from tcc_common.events import publish
class DefenseViewSet(viewsets.ModelViewSet):
 queryset=Defense.objects.all().order_by("date"); serializer_class=DefenseSerializer
 def create(self,request,*a,**kw):
  mid=request.data.get("monograph_id")
  if not mid: return Response({"detail":"monograph_id é obrigatório"},status=400)
  try:
   r=requests.get(f"{__import__('os').getenv('MONOGRAPH_SERVICE_URL','http://monograph-service:8000')}/api/monographs/{mid}/",timeout=5)
   if r.status_code!=200 or not r.json().get("advisor_approved_at"): return Response({"detail":"Monografia ainda não foi aprovada pelo orientador."},status=409)
  except requests.RequestException: return Response({"detail":"Serviço de monografias indisponível."},status=503)
  s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); d=s.save(); publish("defense.scheduled",{"id":str(d.id),"monograph_id":str(d.monograph_id),"date":d.date.isoformat()}); return Response(self.get_serializer(d).data,status=201)
 @action(detail=True,methods=["post"])
 def members(self,request,pk=None):
  d=self.get_object(); s=MemberSerializer(data={**request.data,"defense_id":d.id}); s.is_valid(raise_exception=True); m=s.save(); return Response(MemberSerializer(m).data,status=201)
 @action(detail=True,methods=["post"],url_path="members/(?P<member_id>[^/.]+)/availability")
 def availability(self,request,pk=None,member_id=None):
  m=Member.objects.get(id=member_id,defense_id=pk); m.available=bool(request.data.get("available",True)); m.confirmed_at=timezone.now() if m.available else None; m.save(); return Response(MemberSerializer(m).data)
 @action(detail=True,methods=["post"])
 def evaluations(self,request,pk=None):
  d=self.get_object(); s=EvaluationSerializer(data={**request.data,"defense_id":d.id}); s.is_valid(raise_exception=True); e=s.save(); publish("defense.evaluation_recorded",{"defense_id":str(d.id),"evaluation_id":str(e.id)}); return Response(EvaluationSerializer(e).data,status=201)
 @action(detail=True,methods=["post"])
 def close(self,request,pk=None):
  d=self.get_object(); members=Member.objects.filter(defense_id=d.id); evals=Evaluation.objects.filter(defense_id=d.id)
  if not members.exists() or evals.count()!=members.count(): return Response({"detail":"O resultado só pode ser calculado após todas as avaliações."},status=409)
  d.status=Defense.Status.HELD; d.save(update_fields=["status"]); avg=sum(float(e.grade) for e in evals)/evals.count(); approved=all(e.recommendation!=Evaluation.Recommendation.FAIL for e in evals); publish("defense.completed",{"defense_id":str(d.id),"monograph_id":str(d.monograph_id),"average":avg,"approved":approved}); return Response({"average":avg,"approved":approved})
class ExternalAccessView(viewsets.ViewSet):
 @action(detail=False,methods=["get"],url_path="(?P<token>[^/.]+)")
 def access(self,request,token=None):
  try: m=Member.objects.get(token=token,external=True)
  except Member.DoesNotExist: return Response({"detail":"Token inválido"},status=404)
  return Response({"member":MemberSerializer(m).data,"defense_id":str(m.defense_id)})
