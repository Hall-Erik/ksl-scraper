from rest_framework.serializers import ModelSerializer
from .models import Job, SearchPattern


class JobListSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'employer', 'url', 'date_posted')


class JobCreateSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ('name', 'employer', 'url', 'date_posted')


class SearchPatternSerializer(ModelSerializer):
    class Meta:
        model = SearchPattern
        fields = ('pattern',)
