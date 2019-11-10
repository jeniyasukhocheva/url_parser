from django.db import models
from django.utils import timezone
import requests
from bs4 import BeautifulSoup


class ParserTask(models.Model):
    url = models.URLField()
    start_date = models.DateTimeField('date started')
    minutes = models.IntegerField(default=0)  # todo: >0
    seconds = models.IntegerField(default=0)  # todo: >0 <60
    result = models.OneToOneField(
        to='UrlInfo',
        on_delete=models.CASCADE,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.start_date is None:
            timeshift = timezone.timedelta(
                minutes=self.minutes,
                seconds=self.seconds,
            )
            self.start_date = timezone.now() + timeshift
        super().save(*args, **kwargs)

    def parse_url(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print('ERROR')
            return
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        site_title = soup.title.name
        title = [i.name for i in soup.find_all('h1')]
        charsets = map(lambda x: x.get('charset'), soup.find_all('meta'))
        buf = list(filter(None, charsets))

        if len(buf) != 0:
            encoding = buf[0]
        else:
            encoding = None

        info = UrlInfo(
            site_title=site_title,
            encoding=encoding,
            title='\n'.join(title)
        )
        info.save()
        self.result = info
        self.save()



class UrlInfo(models.Model):
    site_title = models.CharField(max_length=200)
    encoding = models.CharField(max_length=20)
    title = models.TextField()
