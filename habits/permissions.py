from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET для публичных привычек
        if request.method in SAFE_METHODS and obj.is_public:
            return True
        return obj.user == request.user
