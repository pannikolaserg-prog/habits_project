from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность (дни)')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(verbose_name='Время на выполнение (сек)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['time']

    def clean(self):
        # 1. Нельзя заполнять одновременно related_habit и reward
        if self.related_habit and self.reward:
            raise ValidationError('Нельзя указывать и связанную привычку, и вознаграждение одновременно.')

        # 2. У приятной привычки не может быть related_habit или reward
        if self.is_pleasant and (self.related_habit or self.reward):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        # 3. Связанная привычка должна быть приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')

        # 4. Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError('Время выполнения не может превышать 120 секунд.')

        # 5. Периодичность от 1 до 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError('Периодичность должна быть от 1 до 7 дней.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.time}"
