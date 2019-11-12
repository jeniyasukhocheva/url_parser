import logging
import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from url_parser.models import ParserTask

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('url_parser')


class Command(BaseCommand):
    """Command for continual performing parsing"""
    help = 'Wait for tasks and start parsing'

    def handle(self, *args, **options):
        while True:
            logger.info('Searching for tasks')
            now = timezone.now()
            tasks = ParserTask.objects.filter(
                result__isnull=True,
                start_date__lte=now
            )
            for task in tasks:
                logger.info('Parse url ' + task.url)
                task.parse_url()
            time.sleep(1)
