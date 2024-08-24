from rest_framework import viewsets, permissions

from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer

from .permissions import OwnerOrReadOnly, ReadOnly

from .throttling import WorkingHoursRateThrottle

from rest_framework.pagination import PageNumberPagination

from .pagination import CatsPagination

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters




class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Устанавливаем разрешение
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    permission_classes = (OwnerOrReadOnly,)
    #throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle

    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    throttle_scope = 'low_request' 
    # Пагинацию можно установить для отдельного view-класса (для Generics или Viewsets)
    # pagination_class = PageNumberPagination 

    # Вот он наш собственный класс пагинации с page_size=20
    # pagination_class = CatsPagination

    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    # Для сортировки можно подключить встроенный бэкенд OrderingFilter
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    # Временно отключим пагинацию на уровне вьюсета, 
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name', 'achievements__name')
    # поля для сортировки перечисляются в атрибуте ordering_fields
    ordering_fields = ('name', 'birth_year')
    # Упорядочим выдачу по умолчанию по году рождения
    ordering = ('birth_year',)



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions() 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer