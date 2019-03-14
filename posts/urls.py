from django.urls import path, re_path
from posts.views import get_posts, post_detail, create_or_edit_a_post, \
    add_comment_to_post

# CRUD operation url templates
urlpatterns = [
    path('', get_posts, name='get_posts'), 
    path('post/<int:pk>/comment/', add_comment_to_post, 
         name='add_comment_to_post'),
    re_path(r'^(?P<pk>\d+)$', post_detail, name='post_detail'), 
    re_path(r'^new/$', create_or_edit_a_post, name='new_post'),
    re_path(r'^(?P<pk>\d+)/edit/$', create_or_edit_a_post, name='edit_post')
]