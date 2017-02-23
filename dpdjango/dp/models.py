from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class bk_policy(models.Model):
    task = models.CharField(max_length=20)
    client = models.CharField('bak host',max_length=20)
    trees = models.CharField('bak dir',max_length=200)
    drive = models.CharField(max_length=20)
    da = models.CharField(max_length=20)
    script = models.CharField(max_length=20)
    def __str__(self):
        return self.task

@python_2_unicode_compatible
class bk_plan(models.Model):
    policy = models.ForeignKey(bk_policy)
    level = models.CharField(max_length=10)
    protect = models.CharField(max_length=10)
    plan = models.CharField(max_length=20)
    def __str__(self):
        return self.plan
