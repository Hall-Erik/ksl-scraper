from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Job, SearchPattern


class JobListSerializer(ModelSerializer):
    seen = SerializerMethodField()
    
    def get_seen(self, obj):
        user = self.context.get('user')
        return (
            obj.id in user.seenjob_set.all().values_list(
                'job_id', flat=True))


    class Meta:
        model = Job
        fields = (
            'id',
            'name',
            'employer',
            'url',
            'date_posted',
            'seen')


class AllJobListSerializer(ModelSerializer):
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
