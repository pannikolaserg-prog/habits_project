from rest_framework import serializers
from .models import Habit
from .validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        # Вызываем валидацию модели (можно и здесь продублировать)
        # Для удобства используем валидатор из отдельного модуля
        validate_habit(data)
        return data
