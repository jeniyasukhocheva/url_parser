from django.core.management.base import BaseCommand
from url_parser.models import ParserTask
from django.utils import timezone


class Command(BaseCommand):
    help = '1'

    def handle(self, *args, **options):
        while True:
            now = timezone.now()
            tasks = ParserTask.objects.filter(
                result__isnull=True,
                start_date__lte=now
            )

