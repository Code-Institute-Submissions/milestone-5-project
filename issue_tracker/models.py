from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Issue(models.Model):
    """
    The issues list needs allows a user to raise an issue for the
    development team to review.
    """
    title = models.CharField(max_length=140)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True,
                                          default=timezone.now)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=60, blank=True, null=True)
    image = models.ImageField(upload_to="img", blank=True, null=True)
    issue_author = models.ForeignKey(User, default=None,
                                     on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

    class Meta:
        ordering = ['-created_date']

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    """
    Like the blog, a user can comment on an issue posted by another user.
    """
    comment = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, default=None, related_name="issue_comment_author",
        on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, default=None, on_delete=models.CASCADE)
    approved_comment = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment
