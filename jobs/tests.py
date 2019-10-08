from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Job
from .serializers import JobListSerializer
from django.contrib.auth.models import User


class JobListViewTests(TestCase):
    def test_must_be_logged_in(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_jobs(self):
        job = Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        serializer = JobListSerializer(job)
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
        self.assertIn(serializer.data, response.data)

    def test_hidden_jobs_do_not_appear(self):
        job = Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        serializer = JobListSerializer(job)
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        user.hiddenjob_set.create(job_id=job.id)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.assertNotIn(serializer.data, response.data)


class AllJobsListViewTests(TestCase):
    def test_anon_can_access(self):
        response = self.client.get(reverse('jobs:list-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_view_jobs(self):
        job = Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        serializer = JobListSerializer(job)
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('jobs:list-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
        self.assertIn(serializer.data, response.data)

    def test_hidden_jobs_do_not_appear(self):
        job = Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        serializer = JobListSerializer(job)
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        user.hiddenjob_set.create(job_id=job.id)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('jobs:list-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
        self.assertIn(serializer.data, response.data)
