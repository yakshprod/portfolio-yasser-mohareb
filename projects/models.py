from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100)
    image = models.FilePathField(path="projects/static/assets/screenshots")
    def __str__(self):
        return '{} {}'.format(self.id, self.title)
