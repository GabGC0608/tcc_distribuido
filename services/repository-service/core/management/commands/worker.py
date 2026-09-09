from django.core.management.base import BaseCommand
from tcc_common.events import consume
from .models import RepositoryMonograph
from django.utils.dateparse import parse_datetime
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  def cb(event):
   if event["type"]=="monograph.published":
    p=event["payload"]; RepositoryMonograph.objects.update_or_create(id=p["id"],defaults=p)
  consume("repository-worker",["monograph.published"],cb)
