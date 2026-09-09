from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Metric
class Overview(APIView):
 def get(self,request): return Response({"monographs_by_course":{},"monographs_by_advisor":{},"monographs_by_year":{},"approval_rate":None,"average_submission_to_defense":None,"note":"As métricas são atualizadas por eventos; conecte o consumidor ao banco de métricas para agregações em produção."})
class Metrics(APIView):
 def get(self,request): return Response(list(Metric.objects.values("key","value","updated_at")))
