

class DataMixin:
    paginate_by = 5
    title_page = None
    album_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.album_selected is not None:
            self.extra_context['album_selected'] = self.album_selected

    def get_mixin_context(self, context, **kwargs):
        context['album_selected'] = None
        context.update(kwargs)
        return context

