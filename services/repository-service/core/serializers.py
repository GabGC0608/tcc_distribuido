from rest_framework import serializers
from .models import RepositoryMonograph
class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model=RepositoryMonograph
        fields=["id","title","abstract","keywords","author","advisor","course","defense_year","sha256","published_at"]
