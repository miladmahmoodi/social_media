from django import forms
from .models import (
    Post as PostModel,
    Comment as CommentModel,
)


class PostCreateForm(forms.Form):
    caption = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Caption',
            }
        )
    )


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = (
            'caption',
        )
        widgets = {
            'caption': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Caption',
                }
            ),
        }


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = (
            'body',
        )
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Comment',
                }
            ),
        }
        labels = {
            'body': 'Comment',
        }


class PostCommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = (
            'body',
        )
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Comment',
                    'style': 'height:35px',
                },
            ),
        }
        labels = {
            'body': 'Reply',
        }


class PostSearchForm(forms.Form):
    search = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search in posts',
            },
        ),
    )
