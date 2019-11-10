from django.views import generic

from url_parser.models import UrlInfo


class IndexView(generic.ListView):
    template_name = 'url_parser/index.html'
    context_object_name = 'parsed_pages'

    def get_queryset(self):
        return UrlInfo.objects.all()
