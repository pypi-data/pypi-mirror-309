from edu_async_tasks.core.models import RunningTask
from rest_framework import serializers


class RunningTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = RunningTask
        fields = (
            'id',
            'started_at',
            'name',
            'description',
            'status',
            'finished_at',
        )


class RevokeTasksActionSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
