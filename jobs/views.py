from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job, SeenJob
from .serializers import JobListSerializer


class JobListView(ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Job.objects.exclude(
            id__in=user.hiddenjob_set.all().values_list('id', flat=True))


class AllJobsListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    permission_classes = (AllowAny,)


class HideJobView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Job.objects.get(id=id)
        except Job.DoesNotExist:
            raise Http404

    def post(self, request, id):
        user = request.user
        job = self.get_object(id)
        if id not in user.hiddenjob_set.all().values_list(
          'id', flat=True):
            user.hiddenjob_set.create(job=job)
        return Response('success')


class MarkSeenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        new_jobs = Job.objects.exclude(
            id__in=user.seenjob_set.all().values_list('id', flat=True))
        SeenJob.objects.bulk_create([
            SeenJob(user=user, job=job) for job in new_jobs])
        return Response('success')
