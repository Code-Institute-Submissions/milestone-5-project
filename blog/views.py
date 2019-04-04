from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Post, Comment, UserSeenPosts
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator


# Create your views here.

def get_posts(request):
    """
    Create a view that will return a list
    of Posts that were published prior to 'now'
    and render them to the 'blogpost.html' template.
    """
    try:
        blog_list = Post.objects.filter(published_date__lte=timezone.now()
                                    ).order_by('-published_date')
        paginator = Paginator(blog_list, 3)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, "blogposts.html", {'posts': posts})
    except:
        messages.info(request, "There are no posts yet")
        return redirect(reverse('get_posts'))


def post_detail(request, pk):
    """
    Create a view that returns a single
    Post object based on the ID(pk) and
    render it to the 'postdetail.html' template,
    or return an error if the post is not found.
    """
    try:
        post = get_object_or_404(Post, pk=pk)
        if not request.user.seen_posts.filter(post_id=pk).exists():
            post.views += 1
            post.save()
            UserSeenPosts.objects.create(user=request.user, post=post)
        return render(request, "postdetail.html", {'post': post})
    except:
        messages.info(request, "There are no posts yet")
        return redirect(reverse('get_posts'))


def create_or_edit_a_post(request, pk=None):
    """
    Create a view that allows us to create or
    edit a post depending if the Post ID
    is null or not.
    """
    if not request.user or request.user.is_staff or request.user.is_staff:
        post = get_object_or_404(Post, pk=pk) if pk else None
        if request.method == "POST":
            if request.user.is_superuser or request.user.is_staff:
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.published_date = timezone.now()
                    post = form.save()
                    return redirect(post_detail, post.pk)
                else:
                    form = PostForm(instance=post)
                    return render(request, 'blogpostform.html', {'form': form})

        else:
            form = PostForm(instance=post)
            return render(request, 'blogpostform.html', {'form': form})

    else:
        return redirect(reverse('get_posts'))


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)
    else:
        messages.info(request, "A staff member will review your post")         
        return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    else:
        messages.info(request, "Only a staff member can remove a comment.")    
        return redirect('post_detail', pk=comment.post.pk)
