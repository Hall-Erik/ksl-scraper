from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Job
from .serializers import JobListSerializer
from django.contrib.auth.models import User


class JobListViewTests(TestCase):
    def test_must_be_logged_in(self):
        '''Anon user cannot GET this endpoint'''
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_jobs(self):
        '''User can GET a list of jobs'''
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
        '''Hidden jobs are... hidden'''
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
        '''All users can GET this endpoint'''
        response = self.client.get(reverse('jobs:list-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_view_jobs(self):
        '''Can view a list of jobs'''
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

    def test_hidden_jobs_do_appear(self):
        '''Hidden jobs appear in this endpoint'''
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


class HideJobViewTests(TestCase):
    def test_anon_cannot_access(self):
        '''Must be logged in'''
        url = reverse('jobs:hide-job', kwargs={'id': 17})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_hide_jobs(self):
        '''Logged in user can hide jobs'''
        job = Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        url = reverse('jobs:hide-job', kwargs={'id': job.id})
        self.assertEqual(user.hiddenjob_set.count(), 0)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.hiddenjob_set.count(), 1)

    def test_not_found(self):
        '''Bad job id returns a 404'''
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        url = reverse('jobs:hide-job', kwargs={'id': 17})
        self.assertEqual(user.hiddenjob_set.count(), 0)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(user.hiddenjob_set.count(), 0)


class MarkSeenViewTests(TestCase):
    def test_anon_cannot_access(self):
        '''Must be logged in'''
        response = self.client.get(reverse('jobs:mark-seen'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_mark_seen(self):
        '''Logged in user can mark jobs as seen'''
        Job.objects.create(
            name='Test Tech',
            employer='TestCorp',
            url='http://careers.example.com/1',
            date_posted='2019-10-08')
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        self.assertEqual(user.seenjob_set.count(), 0)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('jobs:mark-seen'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.seenjob_set.count(), 1)
