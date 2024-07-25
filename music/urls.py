from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpost/', views.AddPost.as_view(), name='add_post'),
    path('feedback/', views.feedback, name='feedback'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('album/<slug:album_slug>/', views.AlbumList.as_view(), name='album'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag')
]

