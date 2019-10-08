from rest_framework.generics import (
    ListAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job
from .serializers import JobListSerializer


class JobListView(ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Job.objects.exclude(
            id__in=user.hiddenjob_set.all().values_list(
                'id', flat=True))


class AllJobsListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    permission_classes = (AllowAny,)
