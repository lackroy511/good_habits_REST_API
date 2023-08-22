from django.shortcuts import render

from rest_framework import viewsets
from habits.models import Habit

from rest_framework import generics
from habits.pagination import MyPagination

from habits.serializers import HabitCreateSerializer, HabitGetSerializer


# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    
    serializer_class = HabitGetSerializer
    pagination_class = MyPagination
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_serializer_class(self):
        
        if self.action == 'create':
            return HabitCreateSerializer
        
        return HabitGetSerializer
    

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitGetSerializer
    queryset = Habit.objects.filter(is_published=True)
