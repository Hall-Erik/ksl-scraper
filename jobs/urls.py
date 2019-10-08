from django.urls import path
from .views import (
    JobListView,
    AllJobsListView,
    HideJobView)

app_name = 'jobs'

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='list'),
    path('jobs/all/', AllJobsListView.as_view(), name='list-all'),
    path('jobs/<id>/hide/', HideJobView.as_view(), name='hide-job'),
]
