from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from music.models import Post, Album


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'photo', 'post_photo', 'slug', 'content', 'album', 'tags', )
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('tags', )
    list_display = ('id', 'title', 'post_photo', 'time_create', 'is_published', )
    list_display_links = ('id', 'title', )
    ordering = ('time_create', )
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ('set_published', 'set_draft', )
    search_fields = ('title', )
    list_filter = ('album__name', 'is_published', )
    save_on_top = True

    @admin.display(description='Фото', ordering='')
    def post_photo(self, post: Post):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'{count} записей снято с публикации.', messages.WARNING)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


