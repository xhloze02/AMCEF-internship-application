from django.db import models


class Message(models.Model):
    userID = models.IntegerField()
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.title