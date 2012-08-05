from django.views.generic import DetailView, ListView

from ..models import Entry


class EntryDetail(DetailView):
    model = Entry


class TaggedEntryList(ListView):
    template_name = 'blogger/filtered_entry_list.html'
    paginate_by = 10

    def get_queryset(self):
        print self.kwargs
        return Entry.objects.filter(tags__name__in=[self.kwargs['tag']])


class AuthorEntryList(ListView):
    template_name = 'blogger/filtered_entry_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(authors__id__in=[self.kwargs['author_id']])
