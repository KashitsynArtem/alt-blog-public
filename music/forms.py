from django import forms

from music.models import Post, Album


class AddPostForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=Album.objects.all(),
                                   empty_label='Album not selected',
                                   label='Post about',
                                   widget=forms.Select(attrs={'onfocus': 'this.size=6;',
                                                              'onblur': 'this.size=0;',
                                                              'onchange': 'this.size=1; this.blur()'
                                                              }
                                                       )
                                   )

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'album', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }