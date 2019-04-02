from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib import messages
from .models import Issue, Comment
from .forms import AddEditIssueFrom, CommentForm

# Create your views here.


@login_required
def get_issues(request):
    """
    Create a view that will return a list
    of Issues that were published prior to 'now'
    and render them to the 'issues_list.html' template.    
    """
    try:
        issues = Issue.objects.filter(published_date__lte=timezone.now()
                                      ).order_by('-published_date')
        return render(request, "issues_list.html", {'issues': issues})

    except:
        messages.info(request, "There are no issues logged yet")
        return redirect(reverse('get_issues'))


@login_required
def issue_detail(request, pk):
    """
    Create a view that returns a single
    Post object based on the ID(pk) and
    render it to the 'issue_detail.html' template,
    or return an error if the post is not found.
    """    

    issue = get_object_or_404(Issue, pk=pk)
    issue.views += 1
    issue.save()
    return render(request, "issue_detail.html", {'issue': issue})



@login_required
def new_issue(request, pk=None):
    """
    Create a view that allows us to create issue depending if the Issue ID
    is null or not.
    """
    if request.method == "POST":
        form = AddEditIssueFrom(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.author = request.user
            issue = form.save()
            return redirect(get_issues)

    else:
        form = AddEditIssueFrom()
    return render(request, 'new_issue_form.html',
                  {'form': form})


@login_required
def edit_issue(request, pk=None):
    """
    Create a view that allows us to edit an issue based on it product
    key in the issues table.
    """
    issue = get_object_or_404(Issue, pk=pk) if pk else None
    if issue.author == request.user:
        if request.method == "POST":
            form = AddEditIssueFrom(request.POST, request.FILES,
                                    instance=issue)
            if form.is_valid():
                issue = form.save(commit=False)
                issue.author = request.user
                issue = form.save()
                return redirect(reverse('get_issues'))
        else:
            form = AddEditIssueFrom(instance=issue)
    else:
        messages.warning(request,
                         "WARNING! Only the author can edit their bug report")
        return redirect('get_issues')

    return render(request, 'new_issue_form.html',
                  {'form': form})



@login_required
def add_comment_to_issue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.issue = issue
            comment.save()
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_issue.html', {'form': form})


@login_required
def comment_for_issue_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        comment.approve()
        return redirect('issue_detail', pk=comment.issue.pk)
    else:
        messages.info(request, "A staff member will review your post")         
        return redirect('issue_detail', pk=comment.issue.pk)


@login_required
def comment_for_issue_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        comment.delete()
        return redirect('issue_detail', pk=comment.issue.pk)
    else:
        messages.info(request, "Only a staff member can remove a comment.")    
        return redirect('issue_detail', pk=comment.issue.pk)


@login_required
def upvote(request, pk, category):

    issue = get_object_or_404(Issue, pk=pk)
    if category == 'BUG':
        issue.votes += 1
        bug_voter = request.user
        issue.voter.add(bug_voter)
        issue.save()
        return render(request, "issue_detail.html", {'issue': issue})
        messages.info(request, "Thank you for voting.")
    else:
        return redirect(get_issues)
        