import requests
from bs4 import BeautifulSoup
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class ParserTask(models.Model):
    """Model with information about urls that need to be parsed"""
    url = models.URLField()
    start_date = models.DateTimeField('date started')
    minutes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    seconds = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(59)
        ]
    )
    result = models.OneToOneField(
        to='UrlInfo',
        on_delete=models.CASCADE,
        null=True,
        related_name='task',
    )

    def save(self, *args, **kwargs):
        """Calculate start_date based on minutes and seconds"""
        if self.start_date is None:
            timeshift = timezone.timedelta(
                minutes=self.minutes,
                seconds=self.seconds,
            )
            self.start_date = timezone.now() + timeshift
        super().save(*args, **kwargs)

    def parse_url(self):
        """Parse url and create related object with parsing results"""
        try:
            response = requests.get(self.url)
        except Exception as e:
            self.result = UrlInfo.objects.create(
                message='error while requesting. ' + str(e),
                parsed_successful=False,
            )
            self.save()
            return

        if response.status_code != 200:
            self.result = UrlInfo.objects.create(
                message='An error has occurred:' + str(response.status_code),
                parsed_successful=False,
            )
            self.save()
            return

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        site_title = soup.title.text
        title = [i.text for i in soup.find_all('h1')]
        charsets = map(lambda x: x.get('charset'), soup.find_all('meta'))
        buf = list(filter(None, charsets))

        if len(buf) != 0:
            encoding = buf[0]
        else:
            encoding = None

        self.result = UrlInfo.objects.create(
            site_title=site_title,
            encoding=encoding,
            title='\n'.join(title),
            message='page parsed successful',
        )
        self.save()


class UrlInfo(models.Model):
    """Model with information about parsing results of a particular task"""
    message = models.CharField(max_length=200)
    parsed_successful = models.BooleanField(default=True)
    site_title = models.CharField(
        max_length=200,
        null=True
    )
    encoding = models.CharField(
        max_length=20,
        null=True
    )
    title = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def info_for_template(self):
        """Create string to paste it in a template"""
        info = []
        if self.site_title:
            info.append('title: ' + self.site_title)
        if self.encoding:
            info.append('encoding: ' + self.encoding)
        if self.title:
            info.append('h1: ' + self.title.replace('\n', ', '))
        return self.task.url + ' — ' + '; '.join(info) + '\n'
