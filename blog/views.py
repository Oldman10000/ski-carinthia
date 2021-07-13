from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Post
from .forms import BlogPostForm
from profiles.models import UserProfile


def blogs(request):
    """
    returns a list of all posts in reverse time order
    """

    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'date':
                sortkey = 'published_date'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            posts = posts.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('blogs'))

            queries = Q(
                title__icontains=query) | Q(
                    content__icontains=query) | Q(
                        user_profile__user__username__icontains=query) | Q(
                            tag__icontains=query
                        )
            posts = posts.filter(queries)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_sorting = f'{sort}_{direction}'

    context = {
        'search_term': query,
        'page_obj': page_obj,
        'current_sorting': current_sorting,
    }

    return render(request, "blog/blogs.html", context)


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

    return render(request, "blog/post-detail.html", context)


def create_or_edit_post(request, pk=None):
    """
    create a view that allows user to create
    or edit their post
    """

    post = get_object_or_404(Post, pk=pk) if pk else None

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            user = UserProfile.objects.get(user=request.user)
            form.instance.user_profile = user
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
    }

    return render(request, 'blog/blogpost-form.html', context)


def delete_post(request, pk):
    """
    create a view that allows user to delete their post
    """

    post = get_object_or_404(Post, pk=pk)

    post.delete()

    messages.success(
                    request, "Post deleted!")

    return redirect(reverse('blogs'))
