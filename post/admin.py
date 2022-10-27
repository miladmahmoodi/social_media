from django.contrib import admin
from .models import (
    Post as PostModel,
    Comment as CommentModel,
    Like as LikeModel,
)


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'slug',
        'updated_at',
    )
    search_fields = (
        'slug',
        'caption',
    )
    list_filter = (
        'updated_at',
        'slug',
    )
    prepopulated_fields = {
        'slug': ('caption',),
    }
    raw_id_fields = (
        'user',
    )


@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'body',
        'is_reply',
        'created_at',
    )
    search_fields = (
        'body',
        'created_at',
    )
    list_filter = (
        'created_at',
        'is_reply',
    )
    raw_id_fields = (
        'user',
        'post',
        'reply',
    )


@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'created_at',
    )
    search_fields = (
        'user',
        'created_at',
    )
    list_filter = (
        'post',
        'user',
        'created_at',
    )
    raw_id_fields = (
        'user',
        'post',
    )
