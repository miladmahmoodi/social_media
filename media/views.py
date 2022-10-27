from django.shortcuts import render
from django.views import View

from post.models import Post as PostModel
from post.forms import PostSearchForm


class HomeView(View):
    def get(self, request):
        posts = PostModel.objects.all()
        form = PostSearchForm()

        search = request.GET.get('search')
        if search:
            posts = PostModel.objects.filter(
                slug__contains=search,
            )

        return render(
            request,
            'media/content.html',
            {
                'posts': posts,
                'form': form,
            }
        )
