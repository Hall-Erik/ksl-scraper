from django.urls import path
from .views import (
    JobListView,
    AllJobsListView,
    HideJobView,
    MarkJobSeenView,
    MarkSeenView,
    UpdateJobListView,
    SearchPatternListView)

app_name = 'jobs'

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='list'),
    path('jobs/all/', AllJobsListView.as_view(), name='list-all'),
    path('jobs/<id>/hide/', HideJobView.as_view(), name='hide-job'),
    path('jobs/<id>/mark_seen/', MarkJobSeenView.as_view(),
         name='mark-job'),
    path('jobs/mark_seen/', MarkSeenView.as_view(), name='mark-seen'),
    path('jobs/update/', UpdateJobListView.as_view(), name='update-jobs'),
    path('search/', SearchPatternListView.as_view(), name='search'),
]
