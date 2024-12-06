from django_filters import (
    rest_framework as filters,
)

from edu_async_tasks.core.models import (
    RunningTask,
)


class RunningTasksFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('started_at', 'started_at'),
            ('name', 'name'),
            ('description', 'description'),
            ('user_profile', 'user_profile'),
            ('status', 'status__title'),
            ('result', 'result'),
            ('time', 'time'),
        )
    )

    class Meta:
        model = RunningTask
        fields = (
            'started_at',
            'finished_at',
            'name',
            'status',
        )
