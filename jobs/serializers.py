from rest_framework.serializers import ModelSerializer
from .models import Job


class JobListSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'employer', 'url', 'date_posted')
