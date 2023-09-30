from django.db import models

# Create your models here.

class Tasks(models.Model):
    tasktitle = models.CharField(max_length=30)
    taskdesc = models.TextField(max_length=200)

    def __str__(self):
        return self.tasktitle
