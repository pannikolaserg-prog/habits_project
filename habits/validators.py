from rest_framework.serializers import ValidationError


def validate_habit(data):
    related = data.get("related_habit")
    reward = data.get("reward")
    is_pleasant = data.get("is_pleasant", False)
    duration = data.get("duration")
    periodicity = data.get("periodicity", 1)

    if related and reward:
        raise ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение."
        )

    if is_pleasant and (related or reward):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )

    if related and not related.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")

    if duration and duration > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")

    if periodicity < 1 or periodicity > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
