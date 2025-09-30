from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import *


def experience(request):
    companies = (
        Company.objects.filter(is_active=True)
        .prefetch_related("experiences__projects")
        .order_by("name")
    )
    return render(request, "experience.html", {"companies": companies})



class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        return CompanyWriteSerializer if self.action in ["create","update","partial_update"] \
               else CompanyReadSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.select_related("company").prefetch_related("projects")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["company", "employment_type", "start_date", "end_date"]
    search_fields = ["title", "company__name", "description"]
    ordering_fields = ["start_date", "end_date"]
    ordering = ["-start_date"]

    def get_serializer_class(self):
        return ExperienceWriteSerializer if self.action in ["create","update","partial_update"] \
               else ExperienceReadSerializer

    @action(detail=False, url_path="by-company/(?P<company_id>[^/.]+)")
    def by_company(self, company_id=None):
        qs = self.get_queryset().filter(company_id=company_id)
        page = self.paginate_queryset(qs)
        ser = ExperienceReadSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page else Response(ser.data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("experience","experience__company")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["experience"]
    search_fields = ["name", "description", "technologies"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        return ProjectWriteSerializer if self.action in ["create","update","partial_update"] \
               else ProjectReadSerializer

    @action(detail=False, url_path="by-experience/(?P<exp_id>[^/.]+)")
    def by_experience(self, exp_id=None):
        qs = self.get_queryset().filter(experience_id=exp_id)
        page = self.paginate_queryset(qs)
        ser = ProjectReadSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page else Response(ser.data)
