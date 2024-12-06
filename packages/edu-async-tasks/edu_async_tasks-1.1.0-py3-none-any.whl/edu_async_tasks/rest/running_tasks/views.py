from dateutil.relativedelta import (
    relativedelta,
)
from django.utils import (
    timezone,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

import edu_async_tasks
from edu_async_tasks.core.domain.model import (
    TasksNotCancellable,
)
from edu_async_tasks.core.models import (
    RunningTask,
)
from edu_async_tasks.core.services import (
    revoke_async_tasks,
)
from edu_async_tasks.rest.running_tasks.serializers import (
    RevokeTasksActionSerializer,
)
from edu_async_tasks.rest.utils.pagination import (
    LimitOffsetPagination,
)

from .filters import (
    RunningTasksFilter,
)
from .serializers import (
    RunningTaskSerializer,
)


class RunningTasksViewSet(ReadOnlyModelViewSet):

    serializer_class = RunningTaskSerializer
    queryset = RunningTask.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = RunningTasksFilter
    search_fields = ('started_at', 'status__key', 'status__title', 'name')

    @action(detail=False, methods=['post'])
    def revoke(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            revoke_async_tasks(*serializer.validated_data['ids'])
        except TasksNotCancellable as error:
            return Response(status=400, data={'error': str(error)})

        return Response()

    def get_queryset(self):
        return self.queryset.filter(
            started_at__gte=(
                timezone.now() - relativedelta(
                    days=edu_async_tasks.get_config().filter_days_after_start
                )
            )
        )

    def get_serializer_class(self):
        if self.action == 'revoke':
            return RevokeTasksActionSerializer

        return super().get_serializer_class()
