from rest_framework import permissions

# кастомный пермишен OwnerOrReadOnly, который расширит возможности 
# встроенных пермишенов и разрешит полный доступ к объекту только автору
class OwnerOrReadOnly(permissions.BasePermission):

    # Определяет права на уровне запроса и пользователя
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    # Определяет права на уровне объекта
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
