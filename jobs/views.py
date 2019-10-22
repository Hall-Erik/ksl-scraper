from django.http import Http404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny)
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication)
from .models import Job, SeenJob, SearchPattern
from .serializers import (
    JobListSerializer,
    AllJobListSerializer,
    JobCreateSerializer,
    SearchPatternSerializer)


class JobListView(ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get_serializer_context(self):
        user = self.request.user
        return { 'user': user }

    def get_queryset(self):
        user = self.request.user
        return Job.objects.exclude(
            id__in=user.hiddenjob_set.all().values_list('job_id', flat=True))


class AllJobsListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = AllJobListSerializer
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
          'job_id', flat=True):
            user.hiddenjob_set.create(job=job)
        return Response('success')


class MarkJobSeenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Job.objects.get(id=id)
        except Job.DoesNotExist:
            raise Http404

    def post(self, request, id):
        user = request.user
        job = self.get_object(id)
        if id not in user.seenjob_set.all().values_list(
          'job_id', flat=True):
            user.seenjob_set.create(job=job)
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


class UpdateJobListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        url_jobs = request.data
        # Delete jobs that were not included
        Job.objects.exclude(
            url__in=[job for job in url_jobs.keys()]).delete()
        # Check existing jobs for updates
        db_jobs = Job.objects.all()
        for job in db_jobs:
            if job.url in url_jobs.keys() \
              and job.date_posted != url_jobs[job.url]['date_posted']:
                job.date_posted = url_jobs[job.url]['date_posted']
                job.name = url_jobs[job.url]['name']
                job.employer = url_jobs[job.url]['employer']
                job.save()
        # Add New jobs
        new_urls = [
            url for url in url_jobs.keys()
            if url not in db_jobs.values_list('url', flat=True)]
        for url in new_urls:
            serializer = JobCreateSerializer(data=url_jobs[url])
            if serializer.is_valid():
                serializer.save()

        return Response('success')


class SearchPatternListView(ListCreateAPIView):
    queryset = SearchPattern.objects.all()
    serializer_class = SearchPatternSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
