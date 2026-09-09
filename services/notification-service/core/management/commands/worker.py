from django.core.management.base import BaseCommand
from tcc_common.events import consume
from .models import Notification
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  def cb(event):
   t=event["type"]; p=event["payload"]; Notification.objects.create(event_type=t,recipient=str(p.get("student_id") or p.get("advisor_id") or "system"),subject=f"TCC: {t}",message=str(p),sent=True)
  consume("notification-worker",["monograph.*","defense.*"],cb)
