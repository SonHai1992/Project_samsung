from django.db import models

# Create your models here.


class Cadcam(models.Model):
    model = models.CharField(max_length=200)
    process = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    pg_name = models.CharField(max_length=100)
    img = models.ImageField(null=True, blank=True, upload_to='images/')
    type = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=200)


