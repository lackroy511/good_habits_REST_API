from celery.schedules import crontab
from django.shortcuts import render
from rest_framework import generics, viewsets

from habits.models import Habit, ReminderTask
from habits.pagination import MyPagination
from habits.serializers import HabitCreateSerializer, HabitGetSerializer
from habits.services.celery_task_create import create_reminder_task
from habits.services.utils import get_schedule

# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    
    serializer_class = HabitGetSerializer
    pagination_class = MyPagination
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('user')
    
    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        if not habit.is_enjoyable_habit:
            create_reminder_task(habit)
            
    def get_serializer_class(self):
        
        if self.action == 'create':
            return HabitCreateSerializer
        
        return HabitGetSerializer
    

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitGetSerializer
    queryset = Habit.objects.filter(is_published=True).order_by('user')
