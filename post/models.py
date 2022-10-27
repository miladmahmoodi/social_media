from django.db import models
from django.contrib.auth.models import User as UserModel
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    caption = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse(
            'posts:post_create',
        )

    def detail_absolute_url(self):
        return reverse(
            'posts:post_detail',
            args=(
                self.pk,
                self.slug,
            ),
        )

    def delete_absolute_url(self):
        return reverse(
            'posts:post_delete',
            args=(
                self.pk,
            ),
        )

    def update_absolute_url(self):
        return reverse(
            'posts:post_update',
            args=(
                self.pk,
            ),
        )

    def like_absolute_url(self):
        return reverse(
            'posts:post_like',
            args=(
                self.pk,
            ),
        )

    def likes_count(self):
        return self.likes.count()

    def is_like(self, user):
        is_like = user.likes.filter(
            post=self,
        )
        if is_like.exists():
            return True
        return False

    def __str__(self):
        return f'{self.slug} - {self.created_at}'


class Comment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField(
        max_length=400,
    )
    is_reply = models.BooleanField(
        default=False,
    )
    reply = models.ForeignKey(
        'self', # or 'comment'
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = (
            '-created_at',
        )

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user} Like {self.post.slug}'
