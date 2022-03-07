from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CASE_STATUSES = (
    (0, 'New'),
    (1, 'Assigned'),
    (2, 'In Progress'),
    (3, 'Resolved'),
    (4, 'Closed')
)


class Video(models.Model):
    name = models.CharField(max_length=512, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)ss', related_query_name='%(class)s')
    upload_time = models.DateTimeField(auto_now_add=True)
    videofile = models.FileField(upload_to='videos/', null=False, verbose_name='')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=None):
        self.videofile.storage.delete(self.videofile.name)
        super().delete()


class Case(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    pet_name = models.CharField(max_length=64, default='Unnamed pet')
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)ss', related_query_name='%(class)s')
    pet_specialist = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, related_name='assigned_%(class)ss',
                                       related_query_name='assigned_%(class)s', null=True)
    description = models.TextField(help_text='Describe your problem to us :)', null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=CASE_STATUSES, default=0)
    is_public = models.BooleanField(default=False)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)ss')


class Comment(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    comment = models.TextField(help_text='Enter your comment...')
