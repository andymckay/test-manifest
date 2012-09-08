from django.db import models


class Manifest(models.Model):
    sub = models.CharField(max_length=10)
    text = models.TextField()
