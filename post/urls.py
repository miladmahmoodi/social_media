from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='post_create',
    ),
    path(
        '<int:post_id>/<slug:post_slug>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        'delete/<int:post_id>/',
        views.PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        'update/<int:post_id>/',
        views.PostUpdateView.as_view(),
        name='post_update',
    ),
    path(
        'comment/reply/<int:post_id>/<int:comment_id>/',
        views.PostCommentReplyView.as_view(),
        name='reply_comment',
    ),
    path(
        'like/<int:post_id>/',
        views.PostLikeView.as_view(),
        name='post_like',
    ),
]
