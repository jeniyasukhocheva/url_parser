from django.db import models
from django.utils import timezone


class ParserTask(models.Model):
    url = models.URLField()
    start_date = models.DateTimeField('date started')
    minutes = models.IntegerField(default=0)  # todo: >0
    seconds = models.IntegerField(default=0)  # todo: >0 <60
    result = models.OneToOneField('UrlInfo', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.start_date is None:
            timeshift = timezone.timedelta(
                minutes=self.minutes,
                seconds=self.seconds,
            )
            self.start_date = timezone.now() + timeshift
        super().save(*args, **kwargs)


class UrlInfo(models.Model):
    site_title = models.CharField(max_length=200)
    encoding = models.CharField(max_length=20)
    title = models.TextField()
