from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    name = models.CharField(max_length=120)
    employer = models.CharField(max_length=64)
    url = models.CharField(max_length=300, unique=True, db_index=True)
    date_posted = models.CharField(max_length=10)

    class Meta:
        ordering = ['-date_posted', 'employer', 'name']


class SeenJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class HiddenJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SearchPattern(models.Model):
    pattern = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
