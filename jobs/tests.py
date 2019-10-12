from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Job, SearchPattern
from .serializers import JobListSerializer, SearchPatternSerializer
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
        response = self.client.post(url)
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
        response = self.client.post(reverse('jobs:mark-seen'))
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


class UpdateJobListViewTests(TestCase):
    def test_anon_cannot_access(self):
        '''Must be logged in'''
        response = self.client.post(reverse('jobs:update-jobs'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_add_jobs(self):
        '''Logged in user can POST jobs'''
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        data = {
            'jobs':
            [
                {
                    'name': 'tester',
                    'employer': 'testCorp',
                    'url': 'example.com/2',
                    'date_posted': '2019-10-09'
                },
                {
                    'name': 'coder',
                    'employer': 'testCorp',
                    'url': 'example.com/1',
                    'date_posted': '2019-10-10'
                }
            ]
        }
        self.assertEqual(Job.objects.count(), 0)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse('jobs:update-jobs'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.count(), 2)

    def test_user_can_update_jobs(self):
        '''Logged in user can POST job updates'''
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        Job.objects.create(
            name='blah',
            employer='blahblah',
            url='example.com/3',
            date_posted='2019.09.09')
        data = {
            'jobs':
            [
                {
                    'name': 'coder',
                    'employer': 'testCorp',
                    'url': 'example.com/3',
                    'date_posted': '2019-10-10'
                }
            ]
        }
        self.assertEqual(Job.objects.count(), 1)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse('jobs:update-jobs'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Job.objects.get().name, 'coder')
        self.assertEqual(Job.objects.get().employer, 'testCorp')
        self.assertEqual(Job.objects.get().date_posted, '2019-10-10')

    def test_old_jobs_get_deleted(self):
        '''Jobs missing from POST data are deleted'''
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        Job.objects.create(
            name='blah',
            employer='blahblah',
            url='example.com/3',
            date_posted='2019.09.09')
        self.assertEqual(Job.objects.count(), 1)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse('jobs:update-jobs'), {'jobs': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.count(), 0)

    def test_create_update_and_delete(self):
        '''Jobs can be created, updated, and deleted in on POST'''
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123')
        Job.objects.create(
            name='blah',
            employer='blahblah',
            url='example.com/2',
            date_posted='2019.09.09')
        Job.objects.create(
            name='blah',
            employer='blahblah',
            url='example.com/3',
            date_posted='2019.09.09')
        data = {
            'jobs':
            [
                {
                    'name': 'tester',
                    'employer': 'testCorp',
                    'url': 'example.com/2',
                    'date_posted': '2019-10-09'
                },
                {
                    'name': 'coder',
                    'employer': 'testCorp',
                    'url': 'example.com/1',
                    'date_posted': '2019-10-10'
                }
            ]
        }
        self.assertEqual(Job.objects.count(), 2)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse('jobs:update-jobs'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.count(), 2)
        self.assertEqual(
            Job.objects.filter(url='example.com/1').count(), 1)
        self.assertEqual(
            Job.objects.filter(url='example.com/2').count(), 1)
        self.assertEqual(
            Job.objects.filter(url='example.com/3').count(), 0)
        self.assertEqual(
            Job.objects.filter(url='example.com/2').get().name,
            'tester')


class SearchPatternListCreateViewTests(TestCase):
    def test_anon_can_get(self):
        '''Anyone can GET'''
        pattern = SearchPattern.objects.create(
            pattern='software-engineer')
        serializer = SearchPatternSerializer(pattern)
        response = self.client.get(reverse('jobs:search'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, response.data)

    def test_anon_cannot_post(self):
        '''Must be logged in to POST'''
        response = self.client.post(reverse('jobs:search'), {
            'pattern': 'software-engineer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_post(self):
        '''Logged in user can save search patterns'''
        user = User.objects.create_user(username='test')
        client = APIClient()
        client.force_authenticate(user=user)
        self.assertEqual(SearchPattern.objects.count(), 0)
        response = client.post(reverse('jobs:search'), {
            'pattern': 'software-engineer'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SearchPattern.objects.count(), 1)

    def test_no_duplicates_allowed(self):
        '''Can't save the same search pattern twice'''
        SearchPattern.objects.create(pattern='software-engineer')
        user = User.objects.create_user(username='test')
        client = APIClient()
        client.force_authenticate(user=user)
        self.assertEqual(SearchPattern.objects.count(), 1)
        response = client.post(reverse('jobs:search'), {
            'pattern': 'software-engineer'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SearchPattern.objects.count(), 1)
