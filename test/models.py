# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_title = models.CharField(max_length=255, default = '2')
    test_cost = models.CharField(max_length=255, default = "", unique=True)
    test_duration = models.CharField(max_length=20, default = "")
    test_description = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.test_id