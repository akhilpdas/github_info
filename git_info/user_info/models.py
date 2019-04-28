from django.db import models
import jsonfield


# Create your models here.

class UserInfo(models.Model):
    """To save attribute of an entity."""

    username = models.CharField(max_length=100)
    respositories = jsonfield.JSONField(default=dict)
    followers = jsonfield.JSONField(default=dict)
    following = jsonfield.JSONField(default=dict)

class GithubCredentials(models.Model):

    authtoken = models.CharField(max_length=250)