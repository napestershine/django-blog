from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from .models import Post, Category, Tag, Comment
from .forms import CommentForm


def post_list(request):
    posts = Post.published.all()
    template_name = 'blog/index.html'

    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, template_name, {
        'posts': posts,
        page: 'pages'
    })


def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published_on')[:6]

    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    })


def reply_page(request):
    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')

            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url)
        return redirect('/')


def posts_by_category(request, slug):
    template_name = 'blog/post_by_category.html'
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category__slug=slug)

    return render(request, template_name, {
        'posts': posts,
        'category': category
    })


def posts_by_tag(request, slug):
    template_name = 'blog/post_by_tag.html'
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__name=tag)

    return render(request, template_name, {
        'posts': posts,
        'tag': tag
    })
