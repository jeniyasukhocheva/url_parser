import time

from django.core.management.base import BaseCommand
from url_parser.models import ParserTask
from django.utils import timezone


class Command(BaseCommand):
    help = '1'

    def handle(self, *args, **options):
        while True:
            print('eeee, it works!!!!!!')
            now = timezone.now()
            tasks = ParserTask.objects.filter(
                result__isnull=True,
                start_date__lte=now
            )
            for task in tasks:
                print('eeeee, start parsing!!!!!')
                task.parse_url()
            time.sleep(1)
