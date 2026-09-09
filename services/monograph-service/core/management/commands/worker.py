from django.core.management.base import BaseCommand
from django.utils import timezone
from tcc_common.events import consume,publish
from .models import Monograph,ComplementaryDocument
from PyPDF2 import PdfReader
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  def cb(event):
   t=event["type"]; p=event["payload"]
   if t=="monograph.submitted":
    m=Monograph.objects.get(id=p["id"]); reader=PdfReader(m.file.path); text="\n".join((x.extract_text() or "") for x in reader.pages); m.extracted_text=text; m.save(update_fields=["extracted_text","updated_at"]); print("PDF extraído",m.id,flush=True)
   elif t=="defense.completed" and p.get("approved"):
    m=Monograph.objects.get(id=p["monograph_id"]); m.status=Monograph.Status.APPROVED; m.save(update_fields=["status","updated_at"]); has_term=ComplementaryDocument.objects.filter(monograph_id=m.id,type="publication_authorization").exists(); has_correction=ComplementaryDocument.objects.filter(monograph_id=m.id,type="corrected_version").exists()
    if has_term and has_correction:
     m.status=Monograph.Status.PUBLISHED; m.published_at=timezone.now(); m.save(update_fields=["status","published_at","updated_at"]); publish("monograph.published",{"id":str(m.id),"title":m.title,"abstract":m.abstract,"keywords":m.keywords,"author":m.student_name,"advisor":m.advisor_name,"course":m.course_name,"defense_year":m.defense_year,"file_path":m.file.path,"sha256":m.sha256,"published_at":m.published_at.isoformat(),"extracted_text":m.extracted_text})
   elif t=="monograph.authorization_uploaded":
    m=Monograph.objects.get(id=p["monograph_id"]);
    if m.status==Monograph.Status.APPROVED and ComplementaryDocument.objects.filter(monograph_id=m.id,type="corrected_version").exists():
     m.status=Monograph.Status.PUBLISHED; m.published_at=timezone.now(); m.save(update_fields=["status","published_at","updated_at"]); publish("monograph.published",{"id":str(m.id),"title":m.title,"abstract":m.abstract,"keywords":m.keywords,"author":m.student_name,"advisor":m.advisor_name,"course":m.course_name,"defense_year":m.defense_year,"file_path":m.file.path,"sha256":m.sha256,"published_at":m.published_at.isoformat(),"extracted_text":m.extracted_text})
  consume("monograph-worker",["monograph.submitted","defense.completed","monograph.authorization_uploaded"],cb)
