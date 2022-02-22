from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Video(models.Model):
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField('date_uploaded')
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name='')

    # def __str__(self):
    #     return self.name + ': ' + str(self.videofile)
