from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import (
    Post as PostModel,
    Comment as CommentModel,
    Like as LikeModel,
)
from .forms import PostCreateForm, PostUpdateForm,\
    PostCommentForm, PostCommentReplyForm
from utils.base_alerts import BaseAlert


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'post/post_create.html'
    form_class = PostCreateForm

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {'form': form},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            post = PostModel.objects.create(
                user=request.user,
                caption=form_data['caption'],
                slug=slugify(form_data['caption'][:30]),
            )
            messages.success(
                request,
                BaseAlert.success_post_create,
                'success',
            )
            return redirect('posts:post_detail', post.id, post.slug)

        return render(
            request,
            self.template_name,
            {'form': form},
        )


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'post/post_detail.html'
    form_class = PostCommentForm
    form_class_reply = PostCommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            PostModel,
            pk=kwargs['post_id'],
            slug=kwargs['post_slug'],
        )
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.comments.all()
        is_like = False
        if post.is_like(request.user):
            is_like = True

        return render(
            request,
            self.template_name,
            {
                'post': post,
                'comments': comments,
                'form': self.form_class,
                'reply_form': self.form_class_reply,
                'is_like': is_like,
            }
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.post_instance
            comment.save()
            messages.success(
                request,
                BaseAlert.success_create_comment,
                'success',
            )
            return redirect(
                'posts:post_detail',
                self.post_instance.id,
                self.post_instance.slug,
            )
        return render(
            request,
            self.template_name,
            {
                'post': self.post_instance,
                'form': form,
            }
        )


class PostDeleteView(LoginRequiredMixin, View):
    template_name = 'media:home'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            PostModel,
            pk=kwargs['post_id'],
        )
        return super().setup(
            request,
            *args,
            **kwargs
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user != request.user:
            messages.error(
                request,
                BaseAlert.error_delete_post,
                'warning',
            )
            return redirect('accounts:user_login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        post.delete()
        messages.success(
            request,
            BaseAlert.success_delete_post,
            'success',
        )
        return redirect(self.template_name)


class PostUpdateView(LoginRequiredMixin, View):
    template_name = 'post/post_update.html'
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            PostModel,
            pk=kwargs['post_id'],
        )
        return super().setup(
            request,
            *args,
            **kwargs
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user != request.user:
            messages.error(
                request,
                BaseAlert.error_update_post,
                'warning',
            )
            return redirect('accounts:user_login')
        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)

        return render(
            request,
            self.template_name,
            {
                'post': post,
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.slug = slugify(
                form.cleaned_data['caption'][:30]
            )
            form_data.save()
            messages.success(
                request,
                BaseAlert.success_post_update,
                'success',
            )
            return redirect(
                'posts:post_detail',
                post.id,
                post.slug,
            )

        return render(
            request,
            self.template_name,
            {'form':form}
        )


class PostCommentReplyView(LoginRequiredMixin, View):
    template_name = 'post/post_detail.html'
    form_class = PostCommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(
            PostModel,
            pk=post_id,
        )
        comment = get_object_or_404(
            CommentModel,
            pk=comment_id,
        )
        form = self.form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.post = post
            reply_comment.is_reply = True
            reply_comment.reply = comment
            reply_comment.save()
            messages.success(
                request,
                BaseAlert.success_create_comment,
                'success',
            )
            return redirect(
                'posts:post_detail',
                post.id,
                post.slug,
            )
        return render(
            request,
            self.template_name,
            {
                'post': post,
                'form': form,
            }
        )


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(
            PostModel,
            pk=post_id,
        )
        is_liked = LikeModel.objects.filter(
            user=request.user,
            post=post.pk,
        )
        if is_liked:
            is_liked.delete()
            return redirect(
                'posts:post_detail',
                post.id,
                post.slug,
            )

        LikeModel.objects.create(
            user=request.user,
            post=post,
        )
        return redirect(
            'posts:post_detail',
            post.id,
            post.slug,
        )
