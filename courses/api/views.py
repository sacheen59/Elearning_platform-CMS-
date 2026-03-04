from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from courses.api.serializers import SubjectSerializer,CourseSerializer,CourseWithContentSerializer
from courses.api.pagination import StandardPagination
from courses.models import Subject,Course
from courses.api.permissions import IsEnrolled

class SubjectListView(generics.ListAPIView):
    """API view for list of subject."""
    queryset = Subject.objects.annotate(total_courses = Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class SubjectDetailView(generics.RetrieveAPIView):
    """API view for subject detail."""
    queryset = Subject.objects.annotate(total_courses = Count('courses'))
    serializer_class = SubjectSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    """API ViewSet for subject."""
    queryset = Subject.objects.annotate(total_course= Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self,request,*args,**kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(
        detail=True,
        methods='get',
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request,*args,**kwargs)
