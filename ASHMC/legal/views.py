from django.views.generic import DetailView

from .models import Article
# Create your views here.


class DocumentDetail(DetailView):
    model = Article
    def get_queryset(self):
        """We only want root documents here."""
        return Article.objects.filter(level=0)
