from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        # Пользователь видит свои привычки + публичные чужие (только для чтения)
        user = self.request.user
        if self.action == "list" and not self.request.query_params.get("public"):
            # список своих
            return Habit.objects.filter(user=user)
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public")
    def public_list(self, request):
        """Список публичных привычек"""
        habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
