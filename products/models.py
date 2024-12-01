# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, default = '')
    product_type_id = models.CharField(max_length=255, default = "")
    product_company_id = models.CharField(max_length=255, default = "")
    product_price = models.CharField(max_length=255, default = "")
    product_image = models.CharField(max_length=255, null = True)
    product_description = models.TextField(default = "")
    product_stock = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.product_name    
