from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from music.forms import AddPostForm
from music.models import Post, Album, TagPost
from music.utils.mixins import DataMixin


class HomePage(DataMixin, ListView):
    template_name = 'music/home_page.html'
    context_object_name = 'posts'
    title_page = 'Home page'
    album_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('album')


def about(request):
    return render(request, 'music/about.html', {'title': 'About ATL', })


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'music/add_post.html'
    success_url = reverse_lazy('home') # TODO: add reverse message
    title_page = 'Add post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Post
    field = ['title', 'content', 'photo']
    template_name = 'music/add_post.html'
    success_url = reverse_lazy('home')
    title_page = 'Update post'


def feedback(request):
    return redirect('home')


class ShowPost(DataMixin, DetailView):
    template_name = 'music/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])


class AlbumList(DataMixin, ListView):
    template_name = 'music/home_page.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(album__slug=self.kwargs['album_slug']).select_related('album')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        album = context['posts'][0].album
        return self.get_mixin_context(context,
                                      title='Album - ' + album.name,
                                      album_selected=album.pk,
                                      )


class TagPostList(DataMixin, ListView):
    template_name = 'music/home_page.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Tag: ' + tag.tag)

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('album')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

