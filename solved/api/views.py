from rest_framework import status, viewsets 
from problems.models import Problem
from .serializers import ProblemSerializer
from django.shortcuts import get_object_or_404 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from . import permissions 

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly
        
    ]
    
    def perform_create(self, serializer): 
        serializer.save(author=self.request.user) 