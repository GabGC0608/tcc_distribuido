from rest_framework import serializers
from .models import Course,Professor,Student,Monograph,ComplementaryDocument
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"
class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Professor
        fields="__all__"
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
class MonographSerializer(serializers.ModelSerializer):
    class Meta:
        model=Monograph
        fields="__all__"
        read_only_fields=["sha256","status","submitted_at","advisor_approved_at","published_at","extracted_text"]
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ComplementaryDocument
        fields="__all__"
