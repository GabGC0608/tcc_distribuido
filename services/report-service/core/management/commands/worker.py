from django.core.management.base import BaseCommand
from tcc_common.events import consume
from core.models import Metric
from django.db.models import Count
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  def cb(event):
   # Store lightweight event counters. Detailed cross-service aggregation can be added via periodic snapshots.
   key=event["type"]; m, _=Metric.objects.get_or_create(key=f"events.{key}",defaults={"value":{"count":0}}); m.value["count"]=m.value.get("count",0)+1; m.save()
  consume("report-worker",["monograph.*","defense.*"],cb)
