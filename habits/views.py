from django.shortcuts import render

from rest_framework import viewsets
from habits.models import Habit

from rest_framework import generics

from habits.serializers import HabitSerializer


# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    
    serializer_class = HabitSerializer
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_published=True)
