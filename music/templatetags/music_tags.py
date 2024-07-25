from django import template
from django.db.models import Count

import music.views as views
from music.models import Album, TagPost

register = template.Library()


@register.inclusion_tag('music/list_albums.html')
def show_albums(album_selected=0):
    albums = Album.objects.filter(posts__is_published=True).distinct()
    return {'albums': albums, 'album_selected': album_selected}


@register.inclusion_tag('music/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}

