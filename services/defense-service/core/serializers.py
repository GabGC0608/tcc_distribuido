from rest_framework import serializers
from .models import *
class DefenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Defense
        fields="__all__"
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields=["id","defense_id","user_id","name","email","external","token","available","confirmed_at"]
        read_only_fields=["token","confirmed_at"]
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Evaluation
        fields="__all__"
