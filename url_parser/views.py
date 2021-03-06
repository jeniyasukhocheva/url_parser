from django.views import generic

from url_parser.models import UrlInfo


class IndexView(generic.ListView):
    """Page for displaying information about parsed urls"""
    template_name = 'url_parser/index.html'
    context_object_name = 'parsed_pages'
    model = UrlInfo
