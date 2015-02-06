from django.db import models


class TestUser(models.Model):
    username = models.CharField(max_length=255, null=True)
