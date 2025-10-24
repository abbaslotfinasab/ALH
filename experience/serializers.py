from rest_framework import serializers
from .models import Company, Experience, Project

class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "logo", "website", "is_active"]

class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "slug" ,"name", "logo", "website", "is_active"]

class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "experience", "name", "role", "description", "technology", "link_demo", "screenshot"]

class ProjectReadSerializer(serializers.ModelSerializer):
    experience = serializers.StringRelatedField()
    class Meta:
        model = Project
        fields = ["id", "experience", "name", "role", "description", "technology", "link_demo", "screenshot"]

class ExperienceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["id", "company", "title", "employment_type", "start_date", "end_date", "description"]

class ExperienceReadSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    projects = ProjectReadSerializer(many=True, read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    class Meta:
        model = Experience
        fields = ["id", "company", "title", "employment_type", "start_date", "end_date",
                  "description", "is_current", "projects"]
