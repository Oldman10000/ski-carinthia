from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import BlogPostForm


def blogs(request):
    """
    returns a list of all posts in reverse time order
    """

    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(
                request, "You didn't enter any search criteria!")
            return redirect(reverse('blogs'))

        queries = Q(
            name__icontains=query) | Q(description__icontains=query)
        posts = posts.filter(queries)

    context = {
        'posts': posts,
        'search_term': query,
    }

    return render(request, "blogs.html", context)


def post_detail(request, pk):
    """
    returns a single post object
    """

    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()

    context = {
        'post': post,
    }

    return render(request, "post-detail.html", context)


def create_or_edit_post(request, pk=None):
    """
    create a view that allows user to create
    or edit their post
    """

    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.Post, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
    }

    return render(request, 'blogpost-form.html', context)
