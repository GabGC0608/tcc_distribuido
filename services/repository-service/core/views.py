from django.http import FileResponse,Http404
from rest_framework import generics,permissions
from .models import RepositoryMonograph
from .serializers import RepositorySerializer
class PublicList(generics.ListAPIView):
    queryset=RepositoryMonograph.objects.all().order_by("-defense_year","-published_at")
    serializer_class=RepositorySerializer
    permission_classes=[permissions.AllowAny]
    def get_queryset(self):
        qs=super().get_queryset(); p=self.request.query_params
        if p.get("search"):
            q=p["search"]; qs=qs.filter(title__icontains=q) | qs.filter(extracted_text__icontains=q)
        if p.get("author"): qs=qs.filter(author__icontains=p["author"])
        if p.get("advisor"): qs=qs.filter(advisor__icontains=p["advisor"])
        if p.get("course"): qs=qs.filter(course__icontains=p["course"])
        if p.get("year"): qs=qs.filter(defense_year=p["year"])
        if p.get("keyword"): qs=qs.filter(keywords__icontains=p["keyword"])
        return qs.distinct()
class PublicDetail(generics.RetrieveAPIView):
    queryset=RepositoryMonograph.objects.all(); serializer_class=RepositorySerializer; permission_classes=[permissions.AllowAny]
class Download(generics.GenericAPIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request,pk):
        try: o=RepositoryMonograph.objects.get(pk=pk)
        except RepositoryMonograph.DoesNotExist: raise Http404
        return FileResponse(open(o.file_path,"rb"),as_attachment=True,filename=f"{o.title[:80]}.pdf")
